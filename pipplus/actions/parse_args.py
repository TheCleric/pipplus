import argparse
import logging
import sys
from typing import List, Optional, Tuple

from . import help as _help
from . import pipplus_command, run


def process(cli_args: List[str]) -> Optional[argparse.Namespace]:
    cli_args, extras = _parse_extra(cli_args)

    parser = argparse.ArgumentParser(description='Python Package Manager')
    subparsers = parser.add_subparsers(dest='command')

    run.RunCommand(subparsers, extras=extras)

    _help.HelpCommand(subparsers, extras=extras)

    if len(cli_args) < 1:
        parser.print_help()
        return None

    try:
        return parser.parse_args(cli_args)
    except pipplus_command.PipPlusCommandExecutionException as ppcee:
        logging.error(ppcee)
        ppcee.command.print_usage()
        sys.exit(-1)
    except Exception as ex:  # pylint: disable=broad-except
        logging.error(ex)
        parser.print_usage()
        sys.exit(-1)


def _parse_extra(argv: List[str]) -> Tuple[List[str], List[str]]:
    extras = []

    if '--' in argv:
        pivot = argv.index('--')
        extras = argv[pivot + 1:]
        argv = argv[:pivot]

    return argv, extras
