from Task4_funk.figures import Rectangle, Circle, Square, Triangle, Rhombus
from Task4_funk.figures import read_positive, read_text


class Menu4:
    def __init__(self):
        self.current = None

    def create(self, cls):
        self.current = cls.create()

    def create_square_around_circle(self):
        r = read_positive("Radius R: ")
        color = read_text("Color: ")
        label = read_text("Label: ")

        try:
            sq = Rectangle.square_around_circle(r, color, label)
            self.current = sq
        except ValueError as e:
            print("Ошибка:", e)

    def show_info(self):
        if not self.current:
            print("Нет фигуры")
            return

        print(self.current)   # <-- ВАЖНО (строка через format)

    def draw(self):
        if not self.current:
            print("Нет фигуры")
            return

        file = input("Имя файла (Enter - пропустить): ").strip()
        self.current.draw(file if file else None)

    def run(self):
        while True:
            print("""
========= МЕНЮ =========
1 Прямоугольник
2 Круг
3 Квадрат
4 Треугольник
5 Ромб
6 Квадрат около окружности
7 Информация о фигуре
8 Нарисовать
0 Выход
""")
            ch = input("> ").strip()

            if ch == "0":
                break
            elif ch == "1":
                self.create(Rectangle)
            elif ch == "2":
                self.create(Circle)
            elif ch == "3":
                self.create(Square)
            elif ch == "4":
                self.create(Triangle)
            elif ch == "5":
                self.create(Rhombus)
            elif ch == "6":
                self.create_square_around_circle()
            elif ch == "7":
                self.show_info()
            elif ch == "8":
                self.draw()
            else:
                print("Ошибка ввода")


if __name__ == "__main__":
    Menu4().run()