from pathlib import Path

from .checks import run_checks
from .models import Report


def scan_repository(path: str | Path) -> Report:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    findings = run_checks(root)
    score = round(sum(1 for finding in findings if finding.status == "ok") / len(findings) * 100)
    return Report(root.name or str(root), score, findings)

