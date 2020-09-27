import argparse
import logging
import sys
from typing import List, Optional, Tuple

from . import run


def process(cli_args: List[str]) -> Optional[argparse.Namespace]:
    cli_args, extras = _parse_extra(cli_args)

    parser = argparse.ArgumentParser(description='Python Package Manager')
    subparsers = parser.add_subparsers(dest='command')

    run.RunCommand(subparsers, extras=extras)

    parser_help = subparsers.add_parser('help')
    parser_help.add_argument('command', nargs="?", default=None)

    if len(cli_args) < 1:
        parser.print_help()
        return None

    try:
        return parser.parse_args(cli_args)
    except Exception as ex:  # pylint: disable=broad-except
        logging.error(ex)
        sys.exit(-1)


def _parse_extra(argv: List[str]) -> Tuple[List[str], List[str]]:
    extras = []

    if '--' in argv:
        pivot = argv.index('--')
        extras = argv[pivot + 1:]
        argv = argv[:pivot]

    return argv, extras
