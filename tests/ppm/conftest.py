from typing import Dict

import pytest


@pytest.fixture(name='mock_toml')
def _mock_toml() -> Dict:
    return {
        'tool': {
            'ppm': {
                'scripts': {
                    'TESTING': 'TESTING 1 2 3 4',
                    'OS_TESTING': {
                        'nt': 'OS_TESTING 1 2 3 4'
                    }
                }
            }
        }
    }
