import argparse
import os
# import platform
# import subprocess
import sys
from typing import Any, Dict, List, Optional, Sequence, Union

from pipplus.helpers import func_logger

from .pipplus_command import PipPlusCommand, PipPlusCommandExecutionException, SubCommandAction


class RunCommand(PipPlusCommand):
    _CONFIG_SECTION = 'scripts'

    def __init__(self, arg_parser: argparse._SubParsersAction, config_data: Dict,
                 extras: Optional[List[str]] = None) -> None:
        super().__init__(arg_parser, config_data, extras)
        self.parser = arg_parser.add_parser(
            'run-script',
            aliases=['run'],
            description="Run a script set in the [tools.pipplus.scripts] table of the pyproject.toml file"
        )
        self.parser.add_argument(
            'run_command',
            metavar='<command>',
            action=SubCommandAction,
            parent=self,
        )
        self.parser.add_argument('extra', metavar='', nargs="*")

    @func_logger.log
    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        if values not in self.config or not self.config[values]:
            raise PipPlusCommandExecutionException(
                "Could not find script '{}' in [tool.pipplus.{}] in the pyproject.toml file".format(
                    values,
                    self._CONFIG_SECTION,
                ),
                self
            )

        script_value = self.config[values]
        if isinstance(script_value, dict):
            if os.name in script_value:
                script_value = script_value[os.name]
            else:
                raise ValueError(
                    "Could not find os '{}' in in [tool.pipplus.{}.{}] in the pyproject.toml file".format(
                        os.name,
                        self._CONFIG_SECTION,
                        values,
                    )
                )

        command = ' '.join(script_value.split(' ') + (self.extras if self.extras else []))
        command = self._parse_replacements(command)

        print('pipplus run {} => "{}"'.format(values, command))

        # self._execute_subprocess(command)
        sys.exit(RunCommand._execute_system(command))

    @func_logger.log
    def _parse_replacements(self, command: str) -> str:
        for replacement in self.replacements:
            command = command.replace(replacement, self.replacements[replacement])

        return command

    @staticmethod
    @func_logger.log
    def _execute_system(command: str) -> int:
        return os.system(command)

    # Leaving this here to fix later. Does not respect virtual environments
    # def _execute_subprocess(self, command: str) -> None:
    #     venv_launch = ''
    #     is_python = command.lower().startswith('python') \
    #         or command.lower().startswith('pip') \
    #         or command.lower().startswith('pytest')
    #     is_venv = 'VIRTUAL_ENV' in environ
    #     if is_venv and is_python:
    #         if platform.system() == 'Windows':
    #             venv_launch = path.join(environ['VIRTUAL_ENV'], 'Scripts', 'activate') + " && "
    #         else:
    #             venv_launch = '. ' + path.join(environ['VIRTUAL_ENV'], 'bin', 'activate') + " && "

    #     process = subprocess.Popen(venv_launch + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #     while True:
    #         if process.stdout is not None:
    #             output = process.stdout.readline()
    #             print(output.decode('utf-8').strip())

    #         return_code = process.poll()
    #         if return_code is not None:
    #             if process.stdout is not None:
    #                 for output in process.stdout.readlines():
    #                     print(output.decode('utf-8').strip())
    #             if process.stderr is not None:
    #                 for error in process.stderr.readlines():
    #                     print(error.decode('utf-8').strip(), file=sys.stderr)
    #             break
