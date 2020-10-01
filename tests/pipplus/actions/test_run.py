import argparse
import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import pytest

from pipplus.actions import pipplus_command, run


@patch('os.system', MagicMock(return_value=0))
@patch('sys.exit', MagicMock())
def test_run_command(mock_config: Dict) -> None:
    tests_args = ['run', 'TESTING']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run.RunCommand(subparser, mock_config)

    parser.parse_args(tests_args)

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(
        mock_config['scripts']['TESTING']
    )

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock(return_value=0))
@patch('sys.exit', MagicMock())
@patch('os.name', 'nt')
def test_run_command_os(mock_config: Dict) -> None:
    tests_args = ['run', 'OS_TESTING']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run.RunCommand(subparser, mock_config)

    parser.parse_args(tests_args)

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(
        mock_config['scripts']['OS_TESTING']['nt']
    )

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock(return_value=0))  # Shouldn't need it, but just in case
@patch('os.name', 'posix')
def test_run_command_os_missing(mock_config: Dict) -> None:
    tests_args = ['run', 'OS_TESTING']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run.RunCommand(subparser, mock_config)

    with pytest.raises(ValueError):
        parser.parse_args(tests_args)


@patch('os.system', MagicMock(return_value=0))  # Shouldn't need it, but just in case
def test_run_command_bad_script(mock_config: Dict) -> None:
    tests_args = ['run', 'non-existent']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run.RunCommand(subparser, mock_config)

    with pytest.raises(pipplus_command.PipPlusCommandExecutionException):
        parser.parse_args(tests_args)


@patch('os.system', MagicMock(return_value=0))  # Shouldn't need it, but just in case
def test_run_command_no_script(mock_config: Dict) -> None:
    tests_args = ['run']

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    run.RunCommand(subparser, mock_config)

    with pytest.raises(SystemExit):
        parser.parse_args(tests_args)
