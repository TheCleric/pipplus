import sys
from typing import List, Optional

from .actions import parse_args


def main(cli_args: Optional[List[str]] = None) -> None:
    parse_args.process(cli_args[1:] if cli_args else sys.argv[1:])


def setup_main() -> None:
    if __name__ == "__main__":
        main(sys.argv)


setup_main()
