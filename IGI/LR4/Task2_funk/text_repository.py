from __future__ import annotations
from pathlib import Path


class TextRepository:
    """Read and write plain text files."""

    def __init__(self, input_path: str | Path, result_path: str | Path):
        self.input_path = Path(input_path)
        self.result_path = Path(result_path)

    def read_text(self) -> str:
        """Read the source text file and return its content."""
        return self.input_path.read_text(encoding="utf-8")

    def write_result(self, text: str) -> None:
        """Write the processed report to the result file."""
        self.result_path.write_text(text, encoding="utf-8")
