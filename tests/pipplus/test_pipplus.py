import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import pipplus


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_pipplus_main(mock_toml: Dict) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        pipplus.pipplus.main(['pipplus', 'run', 'TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(mock_toml['tool']['pipplus']['scripts']['TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
@patch('pipplus.pipplus.__name__', '__main__')
@patch('sys.argv', ['pipplus', 'run', 'TESTING'])
def test_pipplus_cli_run(mock_toml: Dict) -> None:
    with patch('pipplus.actions.pipplus_command.PipPlusCommand._load_toml', MagicMock(return_value=mock_toml)):
        pipplus.pipplus.setup_main()

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(
        mock_toml['tool']['pipplus']['scripts']['TESTING']
    )

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()
