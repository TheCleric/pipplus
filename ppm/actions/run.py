import argparse
import platform
import pprint
import subprocess
import sys
from os import environ, path, system
from typing import Any, List, Optional, Sequence, Union

from .ppm_command import PPMCommand, SubCommandAction


class RunCommand(PPMCommand):
    _TOML_SECTION = 'scripts'

    def __init__(self, arg_parser: argparse._SubParsersAction, extras: List[str] = [],
                 toml_filename: str = 'pyproject.toml') -> None:
        super(RunCommand, self).__init__(arg_parser, extras, toml_filename)
        run_parser = arg_parser.add_parser(
            'run-script',
            aliases=['run'],
            description="Run a script set in the [tools.ppm.scripts] table of the {}".format(toml_filename),
        )
        run_parser.add_argument(
            'run_command', metavar='<command>',
            action=SubCommandAction,
            parent=self,
        )
        run_parser.add_argument('extra', metavar='', nargs="*")

        self.replacements = {
            '$PROJECT_ROOT': self.project_root
        }

    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        if values not in self.toml or not self.toml[values]:
            raise ValueError(
                "Could not find script '{}' in [tool.ppm.{}] in {}".format(
                    values,
                    self._TOML_SECTION,
                    self.toml_filename
                )
            )

        command = ' '.join(self.toml[values].split(' ') + (self.extras if self.extras else []))

        command = self._parse_replacements(command)

        print('ppm run {} => "{}"'.format(values, command))


        # self._execute_subprocess(command)
        self._execute_system(command)

    def _parse_replacements(self, command: str) -> str:
        for replacement in self.replacements.keys():
            command = command.replace(replacement, self.replacements[replacement])

        return command

    def _execute_system(self, command: str) -> None:
        system(command)

    # Leaving this here to fix later. Does not respect virtual environments
    def _execute_subprocess(self, command: str) -> None:
        venv_launch = ''
        is_python = command.lower().startswith('python') \
            or command.lower().startswith('pip') \
            or command.lower().startswith('pytest')
        is_venv = 'VIRTUAL_ENV' in environ
        if is_venv and is_python:
            if platform.system() == 'Windows':
                venv_launch = path.join(environ['VIRTUAL_ENV'], 'Scripts', 'activate') + " && "
            else:
                venv_launch = '. ' + path.join(environ['VIRTUAL_ENV'], 'bin', 'activate') + " && "

        process = subprocess.Popen(venv_launch + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            if process.stdout is not None:
                output = process.stdout.readline()
                print(output.decode('utf-8').strip())

            return_code = process.poll()
            if return_code is not None:
                if process.stdout is not None:
                    for output in process.stdout.readlines():
                        print(output.decode('utf-8').strip())
                if process.stderr is not None:
                    for error in process.stderr.readlines():
                        print(error.decode('utf-8').strip(), file=sys.stderr)
                break
