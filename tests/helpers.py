from pathlib import Path


def assert_has_extension(resp: dict, ext: str) -> list[Path]:
    if resp.get("error", "") != "":
        raise AssertionError(resp["error"])
    changed = resp.get("changed_files") or []
    if not isinstance(changed, list):
        raise AssertionError(f"changed_files is not a list: {type(changed)}")
    matches = [Path(p) for p in changed if str(p).endswith(ext)]
    if not matches:
        raise AssertionError(f"no {ext} in changed_files: {changed}")
    for p in matches:
        if not p.exists():
            raise AssertionError(f"missing file: {p}")
        if p.stat().st_size <= 0:
            raise AssertionError(f"empty file: {p}")
    return matches
