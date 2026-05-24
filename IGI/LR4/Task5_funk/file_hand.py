from __future__ import annotations

import json
from pathlib import Path

from Task5_funk.item import MatrixReportRes


class MatrixReportRepository:
    """Work with append-only storage for matrix reports."""

    def __init__(self, file_path: str | Path = "result_task5.txt"):
        self.file_path = Path(file_path)

    def append_report(self, report: MatrixReportRes) -> None:
        """Append one report as a JSON line."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(report.to_dict(), ensure_ascii=False) + "\n")

    def read_all_reports(self) -> list[MatrixReportRes]:
        """Read all stored reports."""
        if not self.file_path.exists():
            return []

        reports: list[MatrixReportRes] = []
        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    reports.append(MatrixReportRes.from_dict(json.loads(line)))
        return reports