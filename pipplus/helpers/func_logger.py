import inspect
import logging
import os
import pprint
from typing import Any, Callable, TypeVar

_T = TypeVar("_T")

# pylint: disable=protected-access
logging.basicConfig(level=logging._nameToLevel.get(os.environ.get('LOG_LEVEL', ''), logging.root.level))


def log(func: Callable[..., _T]) -> Callable[..., _T]:
    func_name = str(func)

    try:
        if hasattr(func, '__name__'):
            func_name = getattr(func, '__name__')
        if hasattr(func, '__self__'):
            _self = getattr(func, '__self__')
            if hasattr(_self, '__class__'):
                _class = getattr(_self, '__class__')
                if hasattr(_class, '__name__'):
                    func_name = "{}.{}".format(getattr(_class, '__name___'), func_name)
    except Exception as ex:  # pylint: disable=broad-except
        logging.warning("Encountered error trying to get func_name for %s", str(func), exc_info=ex)

    def _wrapped(*args: Any, **kwargs: Any) -> _T:
        try:
            func_sig = inspect.signature(func)
            if len(func_sig.parameters) >= len(args):
                args_pprint = ''
                args_dict = {}
                for index, arg in enumerate(func_sig.parameters):
                    if index < len(args):
                        args_dict[arg] = args[index]
                    else:
                        if arg not in kwargs:
                            args_dict[arg] = func_sig.parameters[arg].default
                args_pprint = pprint.pformat(args_dict or {})[1:][:-1]
            else:
                args_pprint = pprint.pformat(args or ())[1:][:-2]
            kwargs_pprint = pprint.pformat(kwargs or {})[1:][:-1]
            logging.debug(
                'func_logger:\n%s(\n%s%s)',
                func_name,
                args_pprint + "\n" if args_pprint else '',
                "," + kwargs_pprint + "\n" if kwargs_pprint else ''
            )
        except Exception as ex:  # pylint: disable=broad-except
            logging.warning("Encountered error trying to log function %s", func_name, exc_info=ex)

        result = func(*args, **kwargs)

        try:
            if func_name:
                logging.debug('Result for %s:\n%s', func_name, pprint.pformat(result))
        except Exception as ex:  # pylint: disable=broad-except
            logging.warning("Encountered error trying to log result of function %s", func_name, exc_info=ex)

        return result

    return _wrapped
