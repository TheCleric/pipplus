import argparse
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Union

from pipplus.helpers import func_logger


class SubCommandAction(argparse.Action):
    def __init__(self, option_strings: List[str], dest: str, nargs: Optional[Any] = None, **kwargs: Any) -> None:
        if nargs is not None:
            raise ValueError("nargs not allowed")
        if 'parent' not in kwargs:
            raise ValueError("parent not passed to add_argument with SubCommandAction")

        self.parent = kwargs['parent']
        del kwargs['parent']

        super().__init__(option_strings, dest, **kwargs)

    @func_logger.log
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        self.parent.execute(parser, namespace, values, option_string=None)


class PipPlusCommand(ABC):
    _CONFIG_SECTION: Optional[str] = None

    @property
    def config(self) -> Dict:
        if self._CONFIG_SECTION:
            return self.config_data.get(self._CONFIG_SECTION, {})

        return self.config_data

    @property
    def replacements(self) -> Dict:
        return {key: value for key, value in self.config_data.items() if key.startswith('$')}

    @abstractmethod
    def __init__(self, arg_parser: Union[argparse.ArgumentParser, argparse._SubParsersAction], config_data: Dict,
                 extras: Optional[List[str]] = None) -> None:
        self.extras = extras
        self.config_data = config_data
        self.parser: Optional[argparse.ArgumentParser] = None

    @abstractmethod
    def execute(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                values: Union[str, Sequence[Any], None], option_string: Optional[str] = None) -> None:
        raise NotImplementedError

    @func_logger.log
    def print_usage(self) -> None:
        assert self.parser is not None
        self.parser.print_usage()


class PipPlusCommandExecutionException(Exception):
    def __init__(self, message: str, command: PipPlusCommand):
        super().__init__(message)

        self.command = command
