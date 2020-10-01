import logging
import sys
from typing import List, Optional

from pipplus.helpers import func_logger

from .actions import parse_args


@func_logger.log
def main(cli_args: Optional[List[str]] = None) -> None:
    parse_args.process(cli_args[1:] if cli_args else sys.argv[1:])


def setup_main() -> None:
    if __name__ == "__main__":
        logging.debug('Launching pipplus main with args: %s', sys.argv)
        main(sys.argv)


setup_main()
