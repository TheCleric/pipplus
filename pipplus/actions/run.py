import argparse
import os
# import platform
# import subprocess
import sys
from typing import Any, List, Optional, Sequence, Union

from .pipplus_command import DEFAULT_TOML_FILENAME, PipPlusCommand, SubCommandAction


class RunCommand(PipPlusCommand):
    _TOML_SECTION = 'scripts'

    def __init__(self, arg_parser: argparse._SubParsersAction, extras: Optional[List[str]] = None,
                 toml_filename: str = DEFAULT_TOML_FILENAME) -> None:
        super().__init__(arg_parser, extras, toml_filename)
        self.run_parser = arg_parser.add_parser(
            'run-script',
            aliases=['run'],
            description="Run a script set in the [tools.pipplus.scripts] table of the {}".format(toml_filename),
        )
        self.run_parser.add_argument(
            'run_command',
            metavar='<command>',
            action=SubCommandAction,
            parent=self,
        )
        self.run_parser.add_argument('extra', metavar='', nargs="*")

        self.replacements = {'$PROJECT_ROOT': self.project_root}

    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        if values not in self.toml or not self.toml[values]:
            raise ValueError(
                "Could not find script '{}' in [tool.pipplus.{}] in {}".format(
                    values,
                    self._TOML_SECTION,
                    self.toml_filename,
                )
            )

        script_value = self.toml[values]
        if isinstance(script_value, dict):
            if os.name in script_value:
                script_value = script_value[os.name]
            else:
                raise ValueError(
                    "Could not find os '{}' in in [tool.pipplus.{}.{}] in {}".format(
                        os.name,
                        self._TOML_SECTION,
                        values,
                        self.toml_filename,
                    )
                )

        command = ' '.join(script_value.split(' ') + (self.extras if self.extras else []))
        command = self._parse_replacements(command)

        print('pipplus run {} => "{}"'.format(values, command))

        # self._execute_subprocess(command)
        RunCommand._execute_system(command)

    def _parse_replacements(self, command: str) -> str:
        for replacement in self.replacements:
            command = command.replace(replacement, self.replacements[replacement])

        return command

    @staticmethod
    def _execute_system(command: str) -> None:
        sys.exit(os.system(command))

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
