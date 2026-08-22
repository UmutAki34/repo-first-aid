import json
import tempfile
import unittest
from pathlib import Path

from repo_first_aid.cli import main
from repo_first_aid.scanner import scan_repository


class ScannerTests(unittest.TestCase):
    def make_repo(self, files: dict[str, str]) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        for name, content in files.items():
            file_path = temp_dir / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
        return temp_dir

    def test_complete_repository_scores_full_marks(self):
        repo = self.make_repo({
            "README.md": "# Demo\n## Installation\n## Usage\n## Tests",
            "pyproject.toml": "[project]\nname='demo'",
            "CODE_OF_CONDUCT.md": "Be kind.",
            "CONTRIBUTING.md": "Run tests before opening a PR.",
            "LICENSE": "MIT",
            ".gitignore": ".venv/\n.env",
            ".env.example": "API_KEY=",
            ".github/workflows/ci.yml": "name: CI",
        })
        report = scan_repository(repo)
        self.assertEqual(report.score, 100)
        self.assertEqual(report.errors, 0)

    def test_missing_readme_and_license_are_errors(self):
        repo = self.make_repo({"main.py": "print('hi')"})
        report = scan_repository(repo)
        by_id = {finding.check_id: finding for finding in report.findings}
        self.assertEqual(by_id["docs.readme"].status, "error")
        self.assertEqual(by_id["legal.license"].status, "error")
        self.assertGreater(report.warnings, 0)

    def test_secret_file_is_reported(self):
        repo = self.make_repo({"README.md": "# Demo", ".env": "TOKEN=secret"})
        report = scan_repository(repo)
        finding = next(item for item in report.findings if item.check_id == "security.secret-files")
        self.assertEqual(finding.status, "error")

    def test_json_cli_output_is_parseable(self):
        repo = self.make_repo({"README.md": "# Demo"})
        from contextlib import redirect_stdout
        from io import StringIO

        output = StringIO()
        with redirect_stdout(output):
            exit_code = main([str(repo), "--json"])
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 1)
        self.assertIn("findings", payload)

    def test_invalid_path_returns_user_error(self):
        self.assertEqual(main(["/path/that/does/not/exist"]), 2)


if __name__ == "__main__":
    unittest.main()

