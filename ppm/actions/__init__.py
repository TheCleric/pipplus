import argparse
import sys
from typing import List, Tuple

from . import run

_TOML_FILENAME = 'pyproject.toml'

def process() -> argparse.Namespace:
    sys.argv, extras = _parse_extra(sys.argv)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='Python Package Manager')
    subparsers = parser.add_subparsers(dest='command')

    run.RunCommand(subparsers, extras=extras)

    parser_help = subparsers.add_parser('help')
    parser_help.add_argument('command', nargs="?", default=None)

    namespace = parser.parse_args()

    return namespace

def _parse_extra(argv: List[str]) -> Tuple[List[str], List[str]]:
    extras = []

    if '--' in argv:
        pivot = argv.index('--')
        extras = argv[pivot + 1:]
        argv = argv[:pivot]

    return argv, extras
