import argparse
from typing import Any, Dict, List, Optional, Sequence, Union

import pytest

from pipplus.actions import pipplus_command


class PipPlusCommandTester(pipplus_command.PipPlusCommand):
    _CONFIG_SECTION = 'TEST_COMMAND'

    def __init__(self, arg_parser: Union[argparse.ArgumentParser, argparse._SubParsersAction], config_data: Dict,
                 extras: Optional[List[str]] = None) -> None:
        # pylint: disable=useless-super-delegation
        super().__init__(arg_parser, config_data, extras)

    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        # pylint: disable=useless-super-delegation
        super().execute(parser, namespace, values, option_string)


def test_sub_command_action_nargs() -> None:
    with pytest.raises(ValueError):
        pipplus_command.SubCommandAction([], '', 'NARGS')


def test_sub_command_action_no_parent() -> None:
    with pytest.raises(ValueError):
        pipplus_command.SubCommandAction([], '', None)


def test_pipplus_command_execute(mock_config: Dict) -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    pipplus_cmd = PipPlusCommandTester(subparser, mock_config)

    namespace = parser.parse_args([])

    with pytest.raises(NotImplementedError):
        pipplus_cmd.execute(parser, namespace, None)


def test_pipplis_command_config_filter(mock_config: Dict) -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    pipplus_cmd = PipPlusCommandTester(subparser, mock_config)

    assert pipplus_cmd.config_data is not None
    assert pipplus_cmd.config.get('test')
