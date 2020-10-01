import argparse
from typing import Any, Dict, List, Optional, Sequence, Union

from pipplus.helpers import func_logger

from .pipplus_command import PipPlusCommand, PipPlusCommandExecutionException, SubCommandAction


class HelpCommand(PipPlusCommand):
    def __init__(self, arg_parser: argparse._SubParsersAction, config_data: Dict,
                 extras: Optional[List[str]] = None) -> None:
        super().__init__(arg_parser, config_data, extras)
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

    @func_logger.log
    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        if not values or values not in self.other_commands:
            raise PipPlusCommandExecutionException(
                "Could not find command: {} to get help for".format(values),
                self
            )

        assert isinstance(values, str)

        self.other_commands[values].print_usage()
