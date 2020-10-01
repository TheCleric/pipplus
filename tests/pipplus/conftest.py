from typing import Dict

import pytest


@pytest.fixture(name='mock_config')
def _mock_config() -> Dict:
    return {
        'scripts': {
            'TESTING': 'TESTING 1 2 3 4',
            'OS_TESTING': {
                'nt': 'OS_TESTING 1 2 3 4',
            },
        },
        'TEST_COMMAND': {
            'test': True,
        },
    }
