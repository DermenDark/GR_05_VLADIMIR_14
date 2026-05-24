from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    figure_name = "Фигура"

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def draw(self, file=None):
        pass

    @classmethod
    def get_name(cls):
        return cls.figure_name

    @abstractmethod
    def __str__(self):
        pass