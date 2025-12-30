#!/usr/bin/env python3

from logging import Logger
from subprocess import PIPE, run, CalledProcessError, \
    TimeoutExpired, STDOUT, Popen
from typing import Any

from boxtools.data.access.fileAccess import write_to_file


class DataFetcher:
    """
    A class responsible for fetching data from command line inputs.
    """
    def __init__(self, logger: Logger = None, log_output_path: str = None):
        self.LOGGER = logger
        self.log_output_path = log_output_path

    def fetch_data(self, cmd: str = None,
                   cmd_list: list[str] = None,
                   run_path: str = None,
                   output_path: str = None,
                   silent_mode: bool = False,
                   shell_cmd: bool = False,
                   shell_to_stdout: bool = False,
                   query_timeout: int = 300) -> str:
        """
        :param cmd_list:
        :param cmd:
        :param run_path:
        :param output_path:
        :param silent_mode:
        :param shell_cmd:
        :param shell_to_stdout:
        :param query_timeout:
        :return:
        """
        if cmd is None and (cmd_list is None or len(cmd_list) == 0):
            raise ValueError('fetch_data - Either cmd or cmd_list must be provided.')
        if cmd_list is None or len(cmd_list) == 0:
            cmd_list = cmd.split(' ')
        self.LOGGER.info(f'# fetch_data - Running command :: {' '.join(cmd_list)}')
        try:
            result = run(args=cmd_list,
                         cwd=run_path,
                         stdout=PIPE,
                         stderr=STDOUT,
                         text=True,
                         universal_newlines=True,
                         shell=shell_cmd,
                         timeout=query_timeout)
            output: str = result.stdout
            self.LOGGER.debug(f'fetch_data - result.args >> {result.args}')
            self.LOGGER.debug(f'fetch_data - output >> {output}')
            if output_path is not None:
                write_to_file(file_path=output_path, content=output)
        except TimeoutExpired as e:
            raise e
        except CalledProcessError as e:
            raise e

        return output

    def find_value_in_data(self, data: str, search_key: str, delimiter: str = ' ') -> str | None:
        """
        :param data:
        :param search_key:
        :param delimiter:
        :return:
        """
        for line in data.splitlines():
            if search_key in line:
                parts = line.split(delimiter)
                for part in parts:
                    if search_key in part:
                        value = part.strip()
                        self.LOGGER.debug(f'find_value_in_data >> Found value for key "{search_key}": {value}')
                        return value
        self.LOGGER.debug(f'find_value_in_data >> Key "{search_key}" not found in data.')
        return None

    def fetch_deep_data(self, commands: list[str], run_path: str) -> list[str]:
        """
        Runs each command in its own kubectl exec call for robust, non-interactive automation.
        """
        outputs: list[str] = []
        base_kubectl = commands[0].split('--')[0].strip()
        pod_and_container = commands[0].split('--')[1].strip()
        # Use the actual value of VAULT_AGENT_ADDR from your interactive shell
        vault_agent_addr = "http://127.0.0.1:8100"
        for i, cmd in enumerate(commands[1:]):
            full_cmd = f"{base_kubectl} -- {pod_and_container} /bin/sh -c 'VAULT_ADDR={vault_agent_addr} {cmd}'"
            self.LOGGER.info(f'Running: {full_cmd}')
            try:
                proc = Popen(
                    full_cmd,
                    cwd=run_path,
                    stdout=PIPE,
                    stderr=STDOUT,
                    text=True,
                    shell=True
                )
                output, _ = proc.communicate()
                self.LOGGER.info(f'Output for command {i}: {output}')
                outputs.append(output.strip())
            except Exception as e:
                self.LOGGER.error(f'Error running command {i}: {e}')
                outputs.append("")
        return outputs

    def fetch_chained_data(self, spawn_cmd: str, chained_cmds: list[str], expected_prompt: str = r'[#\$] ') -> list[list[Any]]:
        from pexpect import spawn

        # Start an interactive shell in the pod
        child = spawn(
            command=spawn_cmd,
            encoding='utf-8'
        )
        # Wait for next prompt
        child.expect(expected_prompt)
        # Clear initial prompt from buffer
        _ = child.before

        # Send a harmless command to ensure buffer is clean
        child.sendline('echo READY')
        child.expect('READY')
        child.expect(r'[#\$] ')

        outputs: list[list[Any]] = []

        # Send command(s)
        for chained_cmd in chained_cmds:
            child.sendline(chained_cmd)
            child.expect(expected_prompt)

            output = child.before
            self.LOGGER.debug(f'Output for command {chained_cmd}: {output}')
            outputs.append(output)

        child.sendline('exit')
        child.close()
        return outputs



    def _get_output_lines(self, i: int, marker: str, proc: Popen[str]):
        output_lines: list[Any] = []
        while True:
            line = proc.stdout.readline()
            self.LOGGER.debug(f'Line read: {line!r}')
            if not line:
                self.LOGGER.warning(f'EOF reached before marker for command {i}')
                break
            if marker in line:
                break
            output_lines.append(line.rstrip('\n'))
        return output_lines
