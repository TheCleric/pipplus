import argparse
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from pipplus.actions import help as _help
from pipplus.actions import pipplus_command, run


def test_help_command(mock_toml: Dict, monkeypatch: MonkeyPatch) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['help', 'run']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run_command = run.RunCommand(subparser)
        help_command = _help.HelpCommand(subparser)

        # pylint: disable=protected-access
        assert cast(MagicMock, help_command._load_toml).call_count == 2

        print_usage_mock = MagicMock()
        monkeypatch.setattr(run_command.parser, 'print_usage', print_usage_mock)

        parser.parse_args(tests_args)

        print_usage_mock.assert_called_once()


def test_help_command_bad_command(mock_toml: Dict) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['help', 'non-existant']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        help_command = _help.HelpCommand(subparser)

        # pylint: disable=protected-access
        cast(MagicMock, help_command._load_toml).assert_called_once()

        with pytest.raises(pipplus_command.PipPlusCommandExecutionException):
            parser.parse_args(tests_args)
