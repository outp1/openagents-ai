from __future__ import annotations

import os
from pathlib import Path
from typing import List, TypedDict


class LinkResult(TypedDict):
    created: int
    already: int
    conflicts: int
    conflict_paths: List[str]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def rel_symlink(src: Path, dst: Path) -> tuple[bool, str]:
    """Create a relative symlink from dst -> src.

    Returns (created, status):
      - created True/False
      - status one of: 'created', 'already', 'conflict'
    """
    dst_parent = dst.parent
    dst_parent.mkdir(parents=True, exist_ok=True)

    if dst.exists() or dst.is_symlink():
        # If it's an existing symlink to the same target, treat as already
        try:
            existing_target = os.readlink(dst)
            # If existing_target is relative, resolve relative to dst_parent
            existing_path = (dst_parent / existing_target).resolve()
        except OSError:
            existing_path = None

        if existing_path and existing_path == src.resolve():
            return (False, "already")
        else:
            return (False, "conflict")

    # compute relative path from destination directory to source
    rel = os.path.relpath(src, start=dst_parent)
    os.symlink(rel, dst)
    return (True, "created")


def link_many(sources: List[Path], dest_dir: Path) -> LinkResult:
    res: LinkResult = {"created": 0, "already": 0, "conflicts": 0, "conflict_paths": []}
    ensure_dir(dest_dir)
    for src in sources:
        dst = dest_dir / (src.name)
        created, status = rel_symlink(src, dst)
        if status == "created":
            res["created"] += 1
        elif status == "already":
            res["already"] += 1
        else:
            res["conflicts"] += 1
            res["conflict_paths"].append(str(dst))
    return res
