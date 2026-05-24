from dataclasses import dataclass

@dataclass
class Tree:
    name: str
    count: int
    healthy: int

    @property
    def unhealthy(self) -> int:
        return max(self.count - self.healthy, 0)

    @property
    def percent_unhealthy(self) -> float:
        if self.count == 0:
            return 0.0
        return self.unhealthy * 100 / self.count