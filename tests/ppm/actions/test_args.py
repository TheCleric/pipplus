import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

from ppm.actions import args


def test_parse_extra() -> None:
    # pylint: disable=protected-access
    argv, extra = args._parse_extra(['run', 'test', '--', '-v'])

    assert argv == ['run', 'test']
    assert extra == ['-v']


def test_parse_extra_no_extra() -> None:
    # pylint: disable=protected-access
    argv, extra = args._parse_extra(['run', 'test'])

    assert argv == ['run', 'test']
    assert extra == []


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_process_run(mock_toml: Dict) -> None:
    test_args = ['run', 'TESTING']
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        args.process(test_args)

        # pylint: disable=no-member
        cast(MagicMock, os.system).assert_called_once_with(mock_toml['tool']['ppm']['scripts']['TESTING'])

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once()


@patch('argparse.ArgumentParser.print_help', MagicMock())
def test_process_no_args(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        result = args.process([])

        assert result is None

        # pylint: disable=no-member
        cast(MagicMock, args.argparse.ArgumentParser.print_help).assert_called_once()
