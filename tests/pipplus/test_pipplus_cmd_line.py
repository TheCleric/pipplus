import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import pipplus


@patch('os.system', MagicMock(return_value=0))
@patch('sys.exit', MagicMock())
def test_pipplus_main(mock_config: Dict) -> None:
    with patch('pipplus.actions.parse_args._load_toml', MagicMock(return_value=mock_config)):
        pipplus.pipplus_cmd_line.main(['pipplus', 'run', 'TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(mock_config['scripts']['TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock(return_value=0))
@patch('sys.exit', MagicMock())
@patch('pipplus.pipplus_cmd_line.__name__', '__main__')
@patch('sys.argv', ['pipplus', 'run', 'TESTING'])
def test_pipplus_cli_run(mock_config: Dict) -> None:
    with patch('pipplus.actions.parse_args._load_toml', MagicMock(return_value=mock_config)):
        pipplus.pipplus_cmd_line.setup_main()

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(
        mock_config['scripts']['TESTING']
    )

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()
