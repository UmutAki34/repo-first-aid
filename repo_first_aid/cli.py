import argparse
import json
import sys
from pathlib import Path

from .scanner import scan_repository


STATUS_SYMBOLS = {"ok": "[OK]", "warning": "[!]", "error": "[X]"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Give a GitHub repository a practical first-aid report / Bir GitHub reposu için pratik ilk yardım raporu oluşturur.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path / Repo yolu (default: current directory / mevcut dizin)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print machine-readable JSON / JSON çıktı ver")
    return parser


def render_text(report) -> str:
    lines = [f"Repo First Aid / Repo İlk Yardım: {report.repository}", f"Score / Skor: {report.score}/100", ""]
    for finding in report.findings:
        lines.append(f"{STATUS_SYMBOLS[finding.status]} {finding.title}: {finding.message}")
        lines.append(f"  Suggestion / Öneri: {finding.suggestion}")
    lines.append("")
    lines.append(f"Summary / Özet: {report.errors} errors / hata, {report.warnings} warnings / uyarı")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        report = scan_repository(Path(args.path))
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error / Hata: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0 if report.errors == 0 else 1
