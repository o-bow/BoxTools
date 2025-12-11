#!/usr/bin/env python3
from pathlib import PurePath

from git import Repo, cmd, exc
from boxtools.Logs import LogDisplay, LogLevel


class GitPythonTools:
    LOGGER: LogDisplay

    def __init__(self, project_root_folder: PurePath, log_level: int = LogLevel.SILENT):
        self.project_root_folder = project_root_folder
        self.LOGGER = LogDisplay(app_log_level=log_level).get_log_display()

    @staticmethod
    def get_git_object(path):
        return cmd.Git(path)

    def get_git_origin(self):
        cdt_path = str(self.project_root_folder)
        try:
            repo = Repo(cdt_path)
            return repo.remote()
        except exc.NoSuchPathError as nspe:
            print('Currently defined path "{0}" does not exist. Please run `cdt setup` and configure it. Do not mind this '
                  'message if setup operation is ongoing.'.format(cdt_path))
            return None


    def revert_file(self, git_file_path, branch_name):
        origin = self.get_git_origin()
        cli = self.get_git_repo(origin)
        self.LOGGER.show_command_log('git checkout ' + origin.name + '/' + branch_name + ' -- ' + git_file_path)
        cli.checkout(origin.name + '/' + branch_name, git_file_path)

    @staticmethod
    def get_git_repo(origin=get_git_origin()):
        return origin.repo.git


    def git_fetch_all(self):
        repo = Repo(str(self.project_root_folder))
        for remote in repo.remotes:
            self.LOGGER.show_command_log('git fetch ' + remote.name)
            remote.fetch()

    def git_switch(self, git_object, origin_name, branch_name, cleanup=False):
        self.LOGGER.show_command_log('git switch -f -C ' + branch_name + ' ' + origin_name + '/' + branch_name)
        git_object.execute(['git', 'switch', '-f', '-C', branch_name, origin_name + '/' + branch_name])
        if cleanup:
            self.LOGGER.show_command_log('git clean -f -d')
            git_object.execute(['git', 'clean', '-f', '-d'])


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
