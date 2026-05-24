from matplotlib.colors import is_color_like


class FigureColor:
    def __init__(self, color: str):
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Цвет не может быть пустым")

        if not is_color_like(value):
            raise ValueError("Некорректный цвет (например: red, blue, #FF0000)")

        self._color = value