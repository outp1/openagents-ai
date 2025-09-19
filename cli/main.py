from __future__ import annotations

import curses
from pathlib import Path

from .tui import run


def main() -> None:
    curses.wrapper(run)


if __name__ == "__main__":
    main()
