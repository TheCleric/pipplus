import argparse
from typing import Any, List, Optional, Sequence, Union

from .pipplus_command import DEFAULT_TOML_FILENAME, PipPlusCommand, PipPlusCommandExecutionException, SubCommandAction


class HelpCommand(PipPlusCommand):
    def __init__(self, arg_parser: argparse._SubParsersAction, extras: Optional[List[str]] = None,
                 toml_filename: str = DEFAULT_TOML_FILENAME) -> None:
        super().__init__(arg_parser, extras, toml_filename)
        self.other_commands = arg_parser.choices
        self.parser = arg_parser.add_parser(
            'help',
            description='Display the help for a pipplus/ppm command.',
        )
        self.parser.add_argument(
            'help_command',
            metavar='<command>',
            action=SubCommandAction,
            parent=self,
        )

    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        if not values or values not in self.other_commands:
            raise PipPlusCommandExecutionException(
                "Could not find command: {} to get help for".format(values),
                self
            )

        assert isinstance(values, str)

        self.other_commands[values].print_usage()
