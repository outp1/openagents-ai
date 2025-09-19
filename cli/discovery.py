from __future__ import annotations

from pathlib import Path
from typing import List


def find_markdown(root: Path, subdirs: List[str]) -> List[Path]:
    results: List[Path] = []
    for subdir in subdirs:
        base = root / subdir
        if not base.exists():
            continue
        results.extend([p for p in base.rglob("*.md") if p.is_file()])
    # Deduplicate by resolved path to avoid duplicates if overlapping
    seen = set()
    uniq: List[Path] = []
    for p in results:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return sorted(uniq)


def discover_agents(root: Path) -> List[Path]:
    # Prefer local project agents first
    local = find_markdown(root, ["agents", "agent"])
    if local:
        return local
    # Fallback to packaged registry
    pkg_root = Path(__file__).resolve().parent
    return find_markdown(pkg_root, ["_registry/agents"])


def discover_commands(root: Path) -> List[Path]:
    # Prefer local project commands first
    local = find_markdown(root, ["commands", "command"])
    if local:
        return local
    # Fallback to packaged registry
    pkg_root = Path(__file__).resolve().parent
    return find_markdown(pkg_root, ["_registry/commands"])
