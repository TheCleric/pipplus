import argparse
import os
import pathlib
from typing import Any, List, Optional, Sequence, Union

import pytest

from ppm.actions import ppm_command


class PPMTester(ppm_command.PPMCommand):
    def __init__(self, arg_parser: Union[argparse.ArgumentParser, argparse._SubParsersAction],
                 extras: Optional[List[str]] = None, toml_filename: str = ppm_command.DEFAULT_TOML_FILENAME) -> None:
        # pylint: disable=useless-super-delegation
        super().__init__(arg_parser, extras, toml_filename)

    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        # pylint: disable=useless-super-delegation
        super().execute(parser, namespace, values, option_string)


def test_sub_command_action_nargs() -> None:
    with pytest.raises(ValueError):
        ppm_command.SubCommandAction([], '', 'NARGS')


def test_sub_command_action_no_parent() -> None:
    with pytest.raises(ValueError):
        ppm_command.SubCommandAction([], '', None)


def test_ppm_command_execute() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    ppm_cmd = PPMTester(subparser)

    namespace = parser.parse_args([])

    with pytest.raises(NotImplementedError):
        ppm_cmd.execute(parser, namespace, None)


def test_ppm_command_load_toml() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    ppm_cmd = PPMTester(subparser)

    start_in = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'data')

    # pylint: disable=protected-access
    toml = ppm_cmd._load_toml(ppm_command.DEFAULT_TOML_FILENAME, start_in)

    assert toml is not None


def test_ppm_command_load_toml_recurse_up() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    ppm_cmd = PPMTester(subparser)

    start_in = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'data', ppm_command.DEFAULT_TOML_FILENAME)

    # pylint: disable=protected-access
    toml = ppm_cmd._load_toml(ppm_command.DEFAULT_TOML_FILENAME, start_in)

    assert toml is not None


def test_ppm_command_load_toml_no_toml() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    ppm_cmd = PPMTester(subparser)

    with pytest.raises(ppm_command.TOMLNotFoundException):
        # pylint: disable=protected-access
        ppm_cmd._load_toml(ppm_command.DEFAULT_TOML_FILENAME + '_____', os.path.abspath(os.sep))
