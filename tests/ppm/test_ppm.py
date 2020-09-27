import os
import sys
from typing import Dict, cast
from unittest.mock import MagicMock, patch

import ppm


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
def test_ppm_main(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        ppm.ppm.main(['ppm', 'run', 'TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(mock_toml['tool']['ppm']['scripts']['TESTING'])

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()


@patch('os.system', MagicMock())
@patch('sys.exit', MagicMock())
@patch('ppm.ppm.__name__', '__main__')
@patch('sys.argv', ['ppm', 'run', 'TESTING'])
def test_ppm_cli_run(mock_toml: Dict) -> None:
    with patch('ppm.actions.ppm_command.PPMCommand._load_toml', MagicMock(return_value=mock_toml)):
        ppm.ppm.setup_main()

    # pylint: disable=no-member
    cast(MagicMock, os.system).assert_called_once_with(
        mock_toml['tool']['ppm']['scripts']['TESTING']
    )

    # pylint: disable=no-member
    cast(MagicMock, sys.exit).assert_called_once()
