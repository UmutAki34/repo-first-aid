from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    check_id: str
    title: str
    status: str
    message: str
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Report:
    repository: str
    score: int
    findings: list[Finding]

    @property
    def errors(self) -> int:
        return sum(f.status == "error" for f in self.findings)

    @property
    def warnings(self) -> int:
        return sum(f.status == "warning" for f in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository": self.repository,
            "score": self.score,
            "errors": self.errors,
            "warnings": self.warnings,
            "findings": [finding.to_dict() for finding in self.findings],
        }

