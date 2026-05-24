import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Task4_funk.figure import GeometricFigure
from Task4_funk.color import FigureColor


# ================= UTILS =================
def read_positive(prompt: str) -> float:
    """Read positive float from user."""
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Введите положительное число.")


def read_text(prompt: str) -> str:
    """Read non-empty text from user."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Строка не должна быть пустой.")


def set_limits(ax, xmin, xmax, ymin, ymax, pad_ratio=0.15):
    """Set axis limits with padding."""
    dx = xmax - xmin
    dy = ymax - ymin
    pad_x = dx * pad_ratio if dx > 0 else 1
    pad_y = dy * pad_ratio if dy > 0 else 1

    ax.set_xlim(xmin - pad_x, xmax + pad_x)
    ax.set_ylim(ymin - pad_y, ymax + pad_y)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")


# ================= RECTANGLE =================
class Rectangle(GeometricFigure):
    figure_name = "Прямоугольник"

    @classmethod
    def create(cls):
        """Create rectangle from user input."""
        w = read_positive("Width: ")
        h = read_positive("Height: ")
        color = read_text("Color: ")
        label = read_text("Label: ")
        return cls(w, h, color, label)

    @classmethod
    def square_around_circle(cls, radius: float, color: str, label: str):
        """Create a square circumscribed around a circle with radius R."""
        obj = cls(2 * radius, 2 * radius, color, label)
        obj.circle_radius = radius
        return obj

    def __init__(self, w, h, color, label):
        self.w = w
        self.h = h
        self.color = FigureColor(color)
        self.label = label
        self.circle_radius = None  # used only for square around circle

    def area(self):
        """Calculate rectangle area."""
        return self.w * self.h

    def __str__(self):
        """Return formatted description."""
        return (
            "{name}: цвет {color}, ширина {w}, высота {h}. Площадь = {area:.2f}"
        ).format(
            name=self.get_name(),
            color=self.color.color,
            w=self.w,
            h=self.h,
            area=self.area(),
        )

    def draw(self, file=None):
        """Draw rectangle and optionally save to file."""
        fig, ax = plt.subplots()

        rect = patches.Rectangle(
            (0, 0),
            self.w,
            self.h,
            facecolor=self.color.color,
            edgecolor="black"
        )
        ax.add_patch(rect)

        if self.circle_radius is not None:
            circle = patches.Circle(
                (self.w / 2, self.h / 2),
                self.circle_radius,
                facecolor="none",
                edgecolor="red",
                linewidth=2
            )
            ax.add_patch(circle)

        ax.set_title(self.label)
        set_limits(ax, 0, self.w, 0, self.h)

        if file:
            plt.savefig(file, dpi=300)

        plt.show()
        plt.close(fig)


# ================= CIRCLE =================
class Circle(GeometricFigure):
    figure_name = "Круг"

    @classmethod
    def create(cls):
        """Create circle from user input."""
        r = read_positive("Radius: ")
        color = read_text("Color: ")
        label = read_text("Label: ")
        return cls(r, color, label)

    def __init__(self, r, color, label):
        self.r = r
        self.color = FigureColor(color)
        self.label = label

    def area(self):
        """Calculate circle area."""
        return math.pi * self.r ** 2

    def __str__(self):
        """Return formatted description."""
        return (
            "{name}: цвет {color}, радиус {r}. Площадь = {area:.2f}"
        ).format(
            name=self.get_name(),
            color=self.color.color,
            r=self.r,
            area=self.area(),
        )

    def draw(self, file=None):
        """Draw circle and optionally save to file."""
        fig, ax = plt.subplots()

        circ = patches.Circle(
            (0, 0),
            self.r,
            facecolor=self.color.color,
            edgecolor="black"
        )
        ax.add_patch(circ)

        ax.set_title(self.label)
        set_limits(ax, -self.r, self.r, -self.r, self.r)

        if file:
            plt.savefig(file, dpi=300)

        plt.show()
        plt.close(fig)


# ================= SQUARE =================
class Square(Rectangle):
    figure_name = "Квадрат"

    @classmethod
    def create(cls):
        """Create square from user input."""
        s = read_positive("Side: ")
        color = read_text("Color: ")
        label = read_text("Label: ")
        return cls(s, color, label)

    def __init__(self, s, color, label):
        super().__init__(s, s, color, label)

    def __str__(self):
        """Return formatted description."""
        return (
            "{name}: цвет {color}, сторона {s}. Площадь = {area:.2f}"
        ).format(
            name=self.get_name(),
            color=self.color.color,
            s=self.w,
            area=self.area(),
        )


# ================= TRIANGLE =================
class Triangle(GeometricFigure):
    figure_name = "Треугольник"

    @classmethod
    def create(cls):
        """Create triangle from user input."""
        while True:
            a = read_positive("a: ")
            b = read_positive("b: ")
            c = read_positive("c: ")

            if a + b > c and a + c > b and b + c > a:
                break
            print("Такого треугольника не существует.")

        color = read_text("Color: ")
        label = read_text("Label: ")
        return cls(a, b, c, color, label)

    def __init__(self, a, b, c, color, label):
        self.a = a
        self.b = b
        self.c = c
        self.color = FigureColor(color)
        self.label = label

    def area(self):
        """Calculate triangle area by Heron's formula."""
        s = (self.a + self.b + self.c) / 2
        value = s * (s - self.a) * (s - self.b) * (s - self.c)
        return math.sqrt(max(value, 0.0))

    def __str__(self):
        """Return formatted description."""
        return (
            "{name}: цвет {color}, стороны {a}, {b}, {c}. Площадь = {area:.2f}"
        ).format(
            name=self.get_name(),
            color=self.color.color,
            a=self.a,
            b=self.b,
            c=self.c,
            area=self.area(),
        )

    def draw(self, file=None):
        """Draw triangle and optionally save to file."""
        fig, ax = plt.subplots()

        # Geometrically safer triangle construction:
        # A(0,0), B(c,0), C(x,y)
        x = (self.b**2 + self.c**2 - self.a**2) / (2 * self.c)
        y_sq = max(self.b**2 - x**2, 0.0)
        y = math.sqrt(y_sq)

        points = [(0, 0), (self.c, 0), (x, y)]
        tri = patches.Polygon(
            points,
            facecolor=self.color.color,
            edgecolor="black"
        )
        ax.add_patch(tri)

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.set_title(self.label)
        set_limits(ax, min(xs), max(xs), min(ys), max(ys))

        if file:
            plt.savefig(file, dpi=300)

        plt.show()
        plt.close(fig)


# ================= RHOMBUS =================
class Rhombus(GeometricFigure):
    figure_name = "Ромб"

    @classmethod
    def create(cls):
        """Create rhombus from user input."""
        d1 = read_positive("d1: ")
        d2 = read_positive("d2: ")
        color = read_text("Color: ")
        label = read_text("Label: ")
        return cls(d1, d2, color, label)

    def __init__(self, d1, d2, color, label):
        self.d1 = d1
        self.d2 = d2
        self.color = FigureColor(color)
        self.label = label

    def area(self):
        """Calculate rhombus area."""
        return (self.d1 * self.d2) / 2

    def __str__(self):
        """Return formatted description."""
        return (
            "{name}: цвет {color}, диагонали {d1}, {d2}. Площадь = {area:.2f}"
        ).format(
            name=self.get_name(),
            color=self.color.color,
            d1=self.d1,
            d2=self.d2,
            area=self.area(),
        )

    def draw(self, file=None):
        """Draw rhombus and optionally save to file."""
        fig, ax = plt.subplots()

        points = [
            (0, self.d2 / 2),
            (self.d1 / 2, 0),
            (0, -self.d2 / 2),
            (-self.d1 / 2, 0)
        ]

        rh = patches.Polygon(
            points,
            facecolor=self.color.color,
            edgecolor="black"
        )
        ax.add_patch(rh)

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.set_title(self.label)
        set_limits(ax, min(xs), max(xs), min(ys), max(ys))

        if file:
            plt.savefig(file, dpi=300)

        plt.show()
        plt.close(fig)