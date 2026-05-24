
from typing import List, Optional
from Task1_funk.item import Tree
from Task1_funk.handler import TreeRepository


class TreeService:
    """Business logic layer for tree operations."""

    def __init__(self, repo: TreeRepository):
        self.repo = repo

    def __len__(self) -> int:
        """Return number of trees."""
        return len(self.repo.get_all())

    def get_all(self) -> List[Tree]:
        """Get all trees."""
        return self.repo.get_all()

    def add(self, tree: Tree) -> None:
        """Add new tree."""
        trees = self.repo.get_all()
        trees.append(tree)
        self.repo.save_all(trees)

    def remove(self, name: str) -> None:
        """Remove tree by name."""
        trees = self.repo.get_all()
        trees = [t for t in trees if t.name != name]
        self.repo.save_all(trees)

    def find(self, name: str) -> Optional[Tree]:
        """Find tree by name."""
        return next((t for t in self.repo.get_all() if t.name == name), None)

    def sort_by_count(self, reverse: bool = True) -> List[Tree]:
        """Sort trees by count."""
        return sorted(self.repo.get_all(), key=lambda t: t.count, reverse=reverse)

    def total_count(self) -> int:
        """Total number of trees."""
        return sum(t.count for t in self.repo.get_all())

    def total_healthy(self) -> int:
        """Total healthy trees."""
        return sum(t.healthy for t in self.repo.get_all())

    def total_unhealthy(self) -> int:
        """Total unhealthy trees."""
        return sum(t.unhealthy for t in self.repo.get_all())

    def percent_by_type(self):
        """Percentage of trees by type."""
        trees = self.repo.get_all()
        total = self.total_count()
        if total == 0:
            return []
        return [(t.name, t.count * 100 / total) for t in trees]

    def percent_unhealthy_by_type(self):
        """Percentage of unhealthy trees by type."""
        return [(t.name, t.percent_unhealthy) for t in self.repo.get_all()]