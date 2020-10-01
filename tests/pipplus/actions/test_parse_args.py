import os
import sys
from typing import Any, Dict, cast
from unittest.mock import MagicMock, patch

from pipplus.actions import parse_args


def _thrower(*_args: Any, **kwargs: Any) -> None:
    raise Exception("TEST")


def test_parse_extra() -> None:
    # pylint: disable=protected-access
    argv, extra = parse_args._parse_extra(['run', 'test', '--', '-v'])

    assert argv == ['run', 'test']
    assert extra == ['-v']


def test_parse_extra_no_extra() -> None:
    # pylint: disable=protected-access
    argv, extra = parse_args._parse_extra(['run', 'test'])

    assert argv == ['run', 'test']
    assert extra == []


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_process_run(mock_toml: Dict) -> None:
    test_args = ['run', 'TESTING']
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        parse_args.process(test_args)

        # pylint: disable=no-member
        cast(MagicMock, os.system).assert_called_once_with(mock_toml['tool']['pipplus']['scripts']['TESTING'])

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_process_run_invalid_script(mock_toml: Dict) -> None:
    test_args = ['run', 'TESTING_DOES_NOT_EXIST']
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        parse_args.process(test_args)

        # pylint: disable=no-member
        cast(MagicMock, os.system).assert_not_called()

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once_with(-1)


@patch('argparse.ArgumentParser.print_help', MagicMock())
def test_process_no_args(mock_toml: Dict) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        result = parse_args.process([])

        assert result is None

        # pylint: disable=no-member
        cast(MagicMock, parse_args.argparse.ArgumentParser.print_help).assert_called_once()


@patch('sys.exit', MagicMock())
@patch('argparse.ArgumentParser.parse_args', _thrower)
def test_process_exception_handling(mock_toml: Dict) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        parse_args.process(['help', 'run'])

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once_with(-1)
