import argparse
from abc import ABC, abstractmethod
from os import path
from typing import Any, Dict, List, Optional, Sequence, Union

import toml


class TOMLNotFoundException(Exception):
    pass


class SubCommandAction(argparse.Action):
    def __init__(self, option_strings: List[str], dest: str, nargs: Optional[Any] = None, **kwargs: Any) -> None:
        if nargs is not None:
            raise ValueError("nargs not allowed")
        if 'parent' not in kwargs:
            raise ValueError("parent not passed to add_argument with SubCommandAction")

        self.parent = kwargs['parent']
        del kwargs['parent']

        super(SubCommandAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        self.parent.execute(parser, namespace, values, option_string=None)


class PPMCommand(object):
    _TOML_SECTION: Optional[str] = None

    def __init__(self, arg_parser: Union[argparse.ArgumentParser, argparse._SubParsersAction],
                 extras: List[str] = [], toml_filename: str = 'pyproject.toml') -> None:
        self.toml_filename = toml_filename
        self.extras = extras
        toml = self._load_toml(toml_filename, recurse_up=True).get('tool', {}).get('ppm', {})
        self.toml = toml if not self._TOML_SECTION else toml.get(self._TOML_SECTION, {})

    @abstractmethod
    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        raise NotImplementedError

    def _load_toml(self, toml_filename: str, start_in: str = '.', recurse_up: bool = True) -> Dict:
        if path.exists(start_in):
            toml_path = path.join(start_in, toml_filename)
            if path.exists(toml_path):
                self.project_root = path.realpath(start_in)
                return dict(toml.load(toml_path))

            if recurse_up:
                try:
                    return self._load_toml(toml_filename, path.realpath(path.join('..', start_in)))
                except OSError:
                    pass

        raise TOMLNotFoundException(
            "Could not find {} in {} (recurse_up={})".format(toml_filename, start_in, recurse_up)
        )
