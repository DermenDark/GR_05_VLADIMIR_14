from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class SeriesRow:
    """Store one iteration of the series calculation."""
    n: int
    term: float
    partial_sum: float
    abs_error: float

    def to_dict(self) -> dict[str, Any]:
        """Convert row to dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SeriesRow":
        """Create row from dictionary."""
        return SeriesRow(**data)


@dataclass(slots=True)
class StatsRes:
    """Store statistical results for a sequence."""
    mean_value: float
    median_value: float
    mode_value: float | None
    variance: float
    std_dev: float

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "StatsRes":
        """Create stats from dictionary."""
        return StatsRes(**data)


@dataclass(slots=True)
class ReportRes:
    """Store a full calculation result."""
    x: float
    eps: float
    exact_value: float
    approx_value: float
    iterations: int
    rows: list[SeriesRow] = field(default_factory=list)
    stats: StatsRes | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "x": self.x,
            "eps": self.eps,
            "exact_value": self.exact_value,
            "approx_value": self.approx_value,
            "iterations": self.iterations,
            "rows": [row.to_dict() for row in self.rows],
            "stats": self.stats.to_dict() if self.stats else None,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ReportRes":
        """Create report from dictionary."""
        rows = [SeriesRow.from_dict(row) for row in data.get("rows", [])]
        stats_data = data.get("stats")
        stats = StatsRes.from_dict(stats_data) if stats_data else None

        return ReportRes(
            x=data["x"],
            eps=data["eps"],
            exact_value=data["exact_value"],
            approx_value=data["approx_value"],
            iterations=data["iterations"],
            rows=rows,
            stats=stats,
        )