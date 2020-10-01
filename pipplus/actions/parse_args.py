import argparse
import logging
import os
import pathlib
import sys
from typing import Dict, List, Optional, Tuple, Union

import toml

from ..helpers import func_logger
from . import help as _help
from . import pipplus_command, run

DEFAULT_TOML_FILENAME = 'pyproject.toml'


class TOMLNotFoundException(Exception):
    pass


@func_logger.log
def process(cli_args: List[str]) -> Optional[argparse.Namespace]:
    cli_args, extras = _parse_extra(cli_args)

    pipplus_config = _load_toml(DEFAULT_TOML_FILENAME)

    parser = argparse.ArgumentParser(description='Python Package Manager')
    subparsers = parser.add_subparsers(dest='command')

    run.RunCommand(subparsers, pipplus_config, extras=extras)

    _help.HelpCommand(subparsers, pipplus_config, extras=extras)

    if len(cli_args) < 1:
        parser.print_help()
        return None

    try:
        return parser.parse_args(cli_args)
    except pipplus_command.PipPlusCommandExecutionException as ppcee:
        logging.error(ppcee)
        ppcee.command.print_usage()
        return sys.exit(-1)
    except Exception as ex:  # pylint: disable=broad-except
        logging.error(ex)
        parser.print_usage()
        return sys.exit(-1)


@func_logger.log
def _parse_extra(argv: List[str]) -> Tuple[List[str], List[str]]:
    extras = []

    if '--' in argv:
        pivot = argv.index('--')
        extras = argv[pivot + 1:]
        argv = argv[:pivot]

    return argv, extras


@func_logger.log
def _load_toml(toml_filename: str, start_in: Union[str, pathlib.Path] = '.', recurse_up: bool = True) -> Dict:
    start_in = os.path.realpath(start_in)
    if os.path.exists(start_in):
        toml_path = os.path.join(start_in, toml_filename)
        if os.path.exists(toml_path):
            toml_data = dict(toml.load(toml_path).get('tool', {}).get('pipplus', {}))
            toml_data['$PROJECT_ROOT'] = os.path.realpath(start_in)
            return toml_data

        if recurse_up:
            parent_dir = os.path.realpath(os.path.join(start_in, '..'))
            if os.path.exists(parent_dir) and parent_dir != start_in:
                return _load_toml(toml_filename, parent_dir)

    raise TOMLNotFoundException(
        "Could not find {} in {} (recurse_up={})".format(toml_filename, start_in, recurse_up)
    )
