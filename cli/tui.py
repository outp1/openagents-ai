from __future__ import annotations

import curses
from pathlib import Path
from typing import Dict, List, Tuple

from .discovery import discover_agents, discover_commands
from .linker import link_many


TAB_AGENTS = 0
TAB_COMMANDS = 1


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


class CursesApp:
    def __init__(self, root: Path):
        self.root = root
        self.tab = TAB_AGENTS
        self.query = ""
        self.cursor = 0
        self.scroll = 0
        self.height = 0
        self.width = 0

        self.agents: List[Path] = discover_agents(root)
        self.commands: List[Path] = discover_commands(root)
        self.selected: Dict[Tuple[int, str], bool] = {}
        self.message: str | None = None

    def current_items(self) -> List[Path]:
        items = self.agents if self.tab == TAB_AGENTS else self.commands
        if not self.query:
            return items
        q = self.query.lower()
        return [p for p in items if q in p.name.lower()]

    def toggle_select(self, idx: int) -> None:
        items = self.current_items()
        if 0 <= idx < len(items):
            key = (self.tab, str(items[idx]))
            self.selected[key] = not self.selected.get(key, False)

    def toggle_select_all(self) -> None:
        items = self.current_items()
        # If all currently filtered items selected, unselect; else select all
        all_selected = all(self.selected.get((self.tab, str(p)), False) for p in items)
        for p in items:
            key = (self.tab, str(p))
            self.selected[key] = not all_selected

    def get_selected_paths(self) -> List[Path]:
        items = self.current_items()
        selected = []
        for p in items:
            if self.selected.get((self.tab, str(p)), False):
                selected.append(p)
        return selected

    def draw(self, stdscr) -> None:
        stdscr.clear()
        self.height, self.width = stdscr.getmaxyx()
        # Header
        title = "OpenCode Agents/Commands Linker"
        stdscr.addnstr(0, 0, title.ljust(self.width), self.width, curses.A_REVERSE)

        # Tabs
        tab_agents = " Agents "
        tab_commands = " Commands "
        x = 0
        for i, label in [(TAB_AGENTS, tab_agents), (TAB_COMMANDS, tab_commands)]:
            attr = curses.A_BOLD | (curses.A_REVERSE if self.tab == i else 0)
            stdscr.addnstr(1, x, label, self.width - x, attr)
            x += len(label) + 1

        # Filter line
        filter_line = f"Filter: {self.query}"
        stdscr.addnstr(2, 0, filter_line.ljust(self.width), self.width)

        # List area
        items = self.current_items()
        list_top = 3
        list_bottom = self.height - 2
        list_height = max(0, list_bottom - list_top)

        # Adjust cursor range and scroll
        if items:
            self.cursor = clamp(self.cursor, 0, len(items) - 1)
            if self.cursor < self.scroll:
                self.scroll = self.cursor
            if self.cursor >= self.scroll + list_height:
                self.scroll = self.cursor - list_height + 1
        else:
            self.cursor = 0
            self.scroll = 0

        for i in range(list_height):
            idx = self.scroll + i
            if idx >= len(items):
                break
            p = items[idx]
            checked = self.selected.get((self.tab, str(p)), False)
            mark = "[x]" if checked else "[ ]"
            line = f" {mark} {p.name}"
            attr = curses.A_REVERSE if idx == self.cursor else 0
            stdscr.addnstr(list_top + i, 0, line.ljust(self.width), self.width, attr)

        # Footer with help
        selected_count = len(self.get_selected_paths())
        tab_name = "Agents" if self.tab == TAB_AGENTS else "Commands"
        help_text = (
            f"Tab: {tab_name} | Selected: {selected_count} | Keys: Up/Down PgUp/PgDn Move, Space Select, a All, Tab Switch, Enter Install, Ctrl-L Clear, q/Esc Quit"
        )
        # Avoid writing to the bottom-right cell which can error in curses
        safe_w = max(0, self.width - 1)
        stdscr.addnstr(self.height - 1, 0, help_text.ljust(safe_w), safe_w, curses.A_REVERSE)

        stdscr.refresh()

    def handle_install(self, stdscr) -> None:
        sel = [p for p in (self.agents if self.tab == TAB_AGENTS else self.commands) if self.selected.get((self.tab, str(p)), False)]
        if not sel:
            self.message = "Nothing selected"
            return
        dest = (self.root / ".opencode" / ("agent" if self.tab == TAB_AGENTS else "command"))
        result = link_many(sel, dest)
        # Summary screen
        stdscr.clear()
        lines = [
            "Installation Summary:",
            f"  Created: {result['created']}",
            f"  Already linked: {result['already']}",
            f"  Conflicts: {result['conflicts']}",
        ]
        if result["conflicts"]:
            lines.append("  Conflict paths:")
            for cp in result["conflict_paths"]:
                lines.append(f"    - {cp}")
        lines.append("")
        lines.append("Press any key to return...")
        for i, line in enumerate(lines):
            # Prevent writing into the bottom-right cell
            safe_w = max(0, self.width - 1)
            stdscr.addnstr(i, 0, line[: safe_w], safe_w)
        stdscr.refresh()
        stdscr.getch()
        self.message = None

    def run(self, stdscr) -> None:
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        while True:
            self.draw(stdscr)
            ch = stdscr.getch()
            if ch in (ord('q'), 27):  # q or Esc
                break
            elif ch == 9:  # Tab
                self.tab = TAB_COMMANDS if self.tab == TAB_AGENTS else TAB_AGENTS
                self.cursor = 0
                self.scroll = 0
            elif ch in (curses.KEY_UP, ord('k')):
                self.cursor = max(0, self.cursor - 1)
            elif ch in (curses.KEY_DOWN, ord('j')):
                self.cursor = self.cursor + 1
            elif ch == curses.KEY_NPAGE:  # PageDown
                self.cursor += (self.height - 5)
            elif ch == curses.KEY_PPAGE:  # PageUp
                self.cursor -= (self.height - 5)
            elif ch == ord(' '):
                self.toggle_select(self.cursor)
            elif ch == ord('a'):
                self.toggle_select_all()
            elif ch in (10, 13):  # Enter
                self.handle_install(stdscr)
            elif ch == 12:  # Ctrl-L
                self.query = ""
            elif ch in (curses.KEY_BACKSPACE, 127, 8):
                self.query = self.query[:-1]
            elif 32 <= ch <= 126:  # printable
                self.query += chr(ch)


def run(stdscr) -> None:
    app = CursesApp(Path.cwd())
    app.run(stdscr)
