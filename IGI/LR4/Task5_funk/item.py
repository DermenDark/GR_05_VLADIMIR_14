from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(slots=True)
class MatrixStatsRes:
    """Store statistical results for a matrix."""
    mean_main_diag: float
    median_main_diag: float
    corrcoef_diag: float | None
    variance_main_diag: float
    std_main_diag_numpy: float
    std_main_diag_formula: float

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to a dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "MatrixStatsRes":
        """Create stats from a dictionary."""
        return MatrixStatsRes(**data)


@dataclass(slots=True)
class MatrixReportRes:
    """Store the full matrix report."""
    n: int
    m: int
    low: int
    high: int
    matrix: list[list[int]]
    below_diag_sum: int
    stats: MatrixStatsRes

    def to_dict(self) -> dict[str, Any]:
        """Convert report to a dictionary."""
        return {
            "n": self.n,
            "m": self.m,
            "low": self.low,
            "high": self.high,
            "matrix": self.matrix,
            "below_diag_sum": self.below_diag_sum,
            "stats": self.stats.to_dict(),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "MatrixReportRes":
        """Create report from a dictionary."""
        return MatrixReportRes(
            n=data["n"],
            m=data["m"],
            low=data["low"],
            high=data["high"],
            matrix=data["matrix"],
            below_diag_sum=data["below_diag_sum"],
            stats=MatrixStatsRes.from_dict(data["stats"]),
        )