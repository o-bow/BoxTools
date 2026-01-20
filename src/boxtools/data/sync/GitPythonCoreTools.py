#!/usr/bin/env python3

from datetime import datetime
from logging import Logger, getLogger
from pathlib import PurePath

from git import Repo, cmd, exc, GitCommandError

from boxtools.Logs import LogDisplay, LogLevel
from boxtools.exception.Error import GitException


class GitPythonCoreTools:
    LOGGER: LogDisplay

    def __init__(self, project_root_path: PurePath, log_level: int = LogLevel.SILENT):
        self.project_root_folder = project_root_path
        self.LOGGER = LogDisplay(app_log_level=log_level).get_log_display()

    @staticmethod
    def get_git_object(path):
        return cmd.Git(path)

    def get_git_origin(self):
        cdt_path = str(self.project_root_folder)
        try:
            repo = Repo(cdt_path)
            return repo.remote()
        except exc.NoSuchPathError as _:
            print('Currently defined path "{0}" does not exist. Please run `cdt setup` and configure it. Do not mind this '
                  'message if setup operation is ongoing.'.format(cdt_path))
            return None


    def revert_file(self, git_file_path, branch_name):
        origin = self.get_git_origin()
        cli = self.get_git_repo()
        self.LOGGER.show_command_log('git checkout ' + origin.name + '/' + branch_name + ' -- ' + git_file_path)
        cli.checkout(origin.name + '/' + branch_name, git_file_path)

    def get_git_repo(self):
        return self.get_git_origin().repo.git


    def git_fetch_all(self):
        repo = Repo(str(self.project_root_folder))
        for remote in repo.remotes:
            self.LOGGER.show_command_log('git fetch ' + remote.name)
            remote.fetch()

    def git_switch(self, git_object, origin_name, branch_name, cleanup=False):
        git_cmd: list[str] = ['git', 'switch', '-f', '-C', branch_name, f'{origin_name}/{branch_name}']
        self.LOGGER.show_command_log(" ".join(git_cmd))
        git_object.execute(git_cmd)
        if cleanup:
            self.LOGGER.show_command_log('git clean -f -d')
            git_object.execute(['git', 'clean', '-f', '-d'])

    def get_current_branch(self, git_object):
        self.LOGGER.show_command_log('git rev-parse --abbrev-ref HEAD')
        return git_object.execute(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()

    def is_branch_on_remote(self, git_object, origin_name: str = 'origin', branch_name: str = None):
        if branch_name is None:
            branch_name = self.get_current_branch(git_object)
        self.LOGGER.show_command_log('git ls-remote --heads ' + origin_name + ' ' + branch_name)
        result = git_object.execute(['git', 'ls-remote', '--heads', origin_name, branch_name])
        return len(result.strip()) > 0

    def git_switch_for_path(self, project_path, origin_name, branch_name, cleanup=False):
        git_object = cmd.Git(project_path)
        self.git_switch(git_object, origin_name, branch_name, cleanup)

    def git_pull(self, git_object, remote_branch, local_branch):
        self.LOGGER.show_command_log('git pull ' + remote_branch + ' ' + local_branch)
        return git_object.execute(['git', 'pull', remote_branch, local_branch])

    def git_checkout(self, git_object, file_path):
        self.LOGGER.show_command_log('git checkout HEAD -- ' + file_path)
        git_object.execute(['git', 'checkout', 'HEAD', '--', file_path])

    def git_update_refs(self, git_object):
        self.LOGGER.show_command_log('git remote update')
        git_object.execute(['git', 'remote', 'update'])

    def git_log_for_query(self, git_object, branch_name, query):
        self.LOGGER.show_command_log('git log --grep=' + query + ' --pretty=format:%h ' + branch_name)
        return git_object.execute(['git', 'log', '--grep=' + query, '--pretty=format:%h', branch_name])

    def git_commit_message(self, git_object, commit_id):
        self.LOGGER.show_command_log('git show -s --format=%B ' + commit_id)
        return git_object.execute(['git', 'show', '-s', '--format=%B', commit_id])

    def git_compare(self, git_object, source_branch_name: str, target_branch_name: str):
        self.LOGGER.show_command_log('git log --oneline' + source_branch_name + '..' + target_branch_name)
        return git_object.execute(['git', 'log', '--oneline', source_branch_name + '..' + target_branch_name])


class GitService(GitPythonCoreTools):
    def __init__(self,
                 rollback_local_method,
                 apply_configuration_method,
                 project_root_path: PurePath,
                 logger: Logger = None,
                 do_git_backup: bool = False,
                 log_level: int = LogLevel.SILENT,
                 cleanup_on_switch: bool = False):
        self.logger = logger if logger else getLogger(__name__)
        self.do_git_backups = do_git_backup
        self.apply_configuration = apply_configuration_method
        self.rollback_local_conf = rollback_local_method
        self.cleanup_on_switch = cleanup_on_switch
        super().__init__(project_root_path=project_root_path,
                         log_level=log_level)

    def revert_file_develop(self, git_file_path, branch_name='develop'):
        self.revert_file(git_file_path, branch_name)

    def git_pull_process(self, branch_name='develop'):
        self.logger.debug(' ••• git_pull_process: Start ••• ')
        self.logger.info(' ••• Branch to pull: ' + branch_name)
        project_root_folder = str(self.project_root_folder)
        origin_name = self.get_git_origin().name
        git_log = ''
        g = self.get_git_object(path=project_root_folder)
        # 1 - git checkout (rollback custom configuration)
        self.rollback_local_conf(g)

        # 2 - git update
        try:
            git_log = self.git_pull(g, origin_name, branch_name)
            self.logger.info(' ')
            self.logger.info(git_log)
            self.logger.info(' ')

            self.logger.info(' --> Project files updated')
        except GitCommandError as e:
            #handle_git_error(e, git_log)
            raise GitException(git_log, "Could not retrieve data from remote using Git. Please check your VPN.") from e

        # error check
        if 'conflict' in git_log or 'error' in git_log:
            self.logger.info(' --> Git conflict / error detected -> End of process')
        else:
            # 3 - Re-apply local configurations
            self.apply_configuration()
            self.logger.debug(' ••• Update finished')

    def get_revert_source_branch(self, git_object, origin_name: str = 'origin', default_branch='develop'):
        current_branch: str = self.get_current_branch(git_object=git_object)
        if self.is_branch_on_remote(git_object=git_object, origin_name=origin_name, branch_name=current_branch):
            return current_branch
        else:
            return default_branch


    def handle_git_error(self, error, git_log=None):
        self.logger.info(' ')
        self.logger.info('- An issue happened on Git command execution:')
        self.logger.info(' ')
        self.logger.info(error)
        if git_log:
            self.logger.info(git_log)


    def git_switch_process(self, branch_name='develop'):
        self.logger.debug(' ••• git_switch_process: Start ••• ')
        self.logger.info(' ••• Branch to Switch to: ' + branch_name)
        self.logger.info(' ')

        # 1 - Fetch
        try:
            self.logger.debug(' - executing git fetch')
            self.git_fetch_all()
            self.logger.info(" --> git fetch: done")
        except GitCommandError as e:
            self.handle_git_error(e)

        project_root_folder = str(self.project_root_folder)
        origin_name = self.get_git_origin().name
        g = self.get_git_object(path=project_root_folder)

        if self.do_git_backups:
            self.logger.debug(' - executing git checkout (backup)')
            backup_branch_name = 'backup-' + datetime.now().strftime('%b-%d-%I-T-%H-%M-%S')
            self.logger.info(" --> git checkout (backup): done")
            try:
                g.execute(['git', 'checkout', '-b', backup_branch_name])
            except GitCommandError as e:
                self.handle_git_error(e)

        # 2 - switch (reset)
        try:
            self.logger.debug(' - executing git switch')
            self.git_switch(g, origin_name, branch_name, self.cleanup_on_switch)
            self.logger.info(' --> git switch: done')
        except GitCommandError as e:
            self.handle_git_error(e)

        # 4 - Re-apply local configurations
        self.apply_configuration()

        self.logger.info(' ••• Active local branch is now ' + origin_name + '/' + branch_name + ' and is clean.')
        self.logger.debug(' ••• git_switch_process: End ••• ')


    def git_upgrade_process(self):
        project_root_folder = str(self.project_root_folder)
        g = self.get_git_object(path=project_root_folder)
        try:
            self.git_update_refs(g)
        except GitCommandError as e:
            self.handle_git_error(e)
        # TODO


    def git_branch_search(self, branch_name, query):
        g = self.get_git_object(path=str(self.project_root_folder))
        git_log = ''
        try:
            git_log = self.git_log_for_query(g, branch_name, query)
            for line in git_log.splitlines():
                self.logger.info('[ Commit: ' + line + ' ]')
                self.logger.info(self.git_commit_message(g, line))
        except GitCommandError as e:
            self.handle_git_error(e, git_log)

    def git_diff(self, source_branch_name: str, target_branch_name: str):
        project_root_folder = str(self.project_root_folder)
        g = self.get_git_object(path=project_root_folder)
        try:
            self.git_fetch_all()
            git_log = self.git_compare(g, source_branch_name, target_branch_name)
            for line in git_log.splitlines():
                self.logger.info(' - ' + line)
        except GitCommandError as e:
            self.handle_git_error(e)

    def custom_git_diff(self):
        from boxtools.data.input import ask_for_value
        source_branch = ask_for_value('Source branch (current release):')
        target_branch = ask_for_value('Target branch (holds new code):')
        if '/' not in source_branch:
            source_branch = 'origin/' + source_branch
        if '/' not in target_branch:
            target_branch = 'origin/' + target_branch
        self.logger.info('')
        self.logger.debug('=> Executing git diff between ' + source_branch + ' & ' + target_branch + '.')
        self.logger.debug('')
        self.git_diff(source_branch, target_branch)