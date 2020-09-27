import argparse
import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import pytest

from ppm.actions import ppm_command, run


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_run_command(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['run', 'TESTING']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run_command = run.RunCommand(subparser)

        # pylint: disable=protected-access
        cast(MagicMock, run_command._load_toml).assert_called_once_with(
            ppm_command.DEFAULT_TOML_FILENAME,
            recurse_up=True
        )

        parser.parse_args(tests_args)

        # pylint: disable=no-member
        cast(MagicMock, os.system).assert_called_once_with(
            mock_toml['tool']['ppm']['scripts']['TESTING']
        )

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
@patch('os.name', 'nt')
def test_run_command_os(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['run', 'OS_TESTING']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run_command = run.RunCommand(subparser)

        # pylint: disable=protected-access
        cast(MagicMock, run_command._load_toml).assert_called_once_with(
            ppm_command.DEFAULT_TOML_FILENAME,
            recurse_up=True
        )

        parser.parse_args(tests_args)

        # pylint: disable=no-member
        cast(MagicMock, os.system).assert_called_once_with(
            mock_toml['tool']['ppm']['scripts']['OS_TESTING']['nt']
        )

        # pylint: disable=no-member
        cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock())  # Shouldn't need it, but just in case
@patch('os.name', 'posix')
def test_run_command_os_missing(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['run', 'OS_TESTING']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run.RunCommand(subparser)

        with pytest.raises(ValueError):
            parser.parse_args(tests_args)


@patch('os.system', MagicMock())  # Shouldn't need it, but just in case
def test_run_command_bad_script(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['run', 'non-existent']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run_command = run.RunCommand(subparser)

        # pylint: disable=protected-access
        cast(MagicMock, run_command._load_toml).assert_called_once_with(
            ppm_command.DEFAULT_TOML_FILENAME,
            recurse_up=True
        )

        with pytest.raises(ValueError):
            parser.parse_args(tests_args)


@patch('os.system', MagicMock())  # Shouldn't need it, but just in case
def test_run_command_no_script(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        tests_args = ['run']

        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        run_command = run.RunCommand(subparser)

        # pylint: disable=protected-access
        cast(MagicMock, run_command._load_toml).assert_called_once_with(
            ppm_command.DEFAULT_TOML_FILENAME,
            recurse_up=True
        )

        with pytest.raises(SystemExit):
            parser.parse_args(tests_args)
