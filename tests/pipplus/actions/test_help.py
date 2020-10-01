import argparse
from typing import Dict
from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from pipplus.actions import help as _help
from pipplus.actions import pipplus_command, run


def test_help_command(mock_config: Dict, monkeypatch: MonkeyPatch) -> None:
    tests_args = ['help', 'run']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run_command = run.RunCommand(subparser, mock_config)
    _help.HelpCommand(subparser, mock_config)

    print_usage_mock = MagicMock()
    monkeypatch.setattr(run_command.parser, 'print_usage', print_usage_mock)

    parser.parse_args(tests_args)

    print_usage_mock.assert_called_once()


def test_help_command_bad_command(mock_config: Dict) -> None:
    tests_args = ['help', 'non-existant']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    _help.HelpCommand(subparser, mock_config)

    with pytest.raises(pipplus_command.PipPlusCommandExecutionException):
        parser.parse_args(tests_args)
