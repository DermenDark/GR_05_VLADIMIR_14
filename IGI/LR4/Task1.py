from Task1_funk.handler import CsvTreeRepository, PickleTreeRepository
from Task1_funk.arifm_data import TreeService
from Task1_funk.item import Tree
'''
Исходные данные представляют собой словарь.
Необходимо поместить их в файл, используя сериализатор.
Организовать считывание данных, поиск, сортировку в соответствии
с индивидуальным заданием.
Обязательно использовать классы.
Реализуйте два варианта: 1)формат файлов CSV; 2)модуль pickle

Хранятся сведения о лесе:
    вид дерева, общая численность, численность здоровых деревьев.

Составьте программу вычисления:
    1) суммарного числа деревьев на контрольном участке;
    2) суммарного числа здоровых деревьев;
    3) относительную численность (%) больных деревьев;
    4) относительную численность (%) различных видов,
    в том числе больных (%) для каждого вида.

Выведите информацию о виде дерева, введенном с клавиатуры'''


class Menu1:
    def __init__(self):
        self.csv_service = TreeService(CsvTreeRepository("forest.csv"))
        self.pickle_service = TreeService(PickleTreeRepository("forest.pkl"))
        self.current_service = self.csv_service
        self.current_name = "CSV"

    def choose_storage(self):
        print("\n1 - CSV")
        print("2 - pickle")
        choice = input("Выбор хранилища: ").strip()

        if choice == "1":
            self.current_service = self.csv_service
            self.current_name = "CSV"
            print("Выбрано CSV.")
        elif choice == "2":
            self.current_service = self.pickle_service
            self.current_name = "pickle"
            print("Выбрано pickle.")
        else:
            print("Некорректный выбор.")

    def read_current(self):
        trees = self.current_service.get_all()
        if not trees:
            print("Список пуст.")
            return

        for tree in trees:
            print(tree)

    def add_tree(self):
        name = input("Название дерева: ").strip()
        try:
            count = int(input("Общая численность: "))
            healthy = int(input("Численность здоровых: "))
        except ValueError:
            print("Числа введены неверно.")
            return

        if count < 0 or healthy < 0:
            print("Числа не могут быть отрицательными.")
            return

        if healthy > count:
            print("Здоровых деревьев не может быть больше, чем общей численности.")
            return

        self.current_service.add(Tree(name=name, count=count, healthy=healthy))
        print("Запись добавлена.")

    def remove_tree(self):
        name = input("Название для удаления: ").strip()
        self.current_service.remove(name)
        print("Удаление выполнено.")

    def find_tree(self):
        name = input("Название для поиска: ").strip()
        tree = self.current_service.find(name)
        if tree is None:
            print("Дерево не найдено.")
        else:
            print(tree)

    def show_stats(self):
        print("Всего деревьев:", self.current_service.total_count())
        print("Здоровых деревьев:", self.current_service.total_healthy())
        print("Больных деревьев:", self.current_service.total_unhealthy())
        print("Процент видов от общего числа:", self.current_service.percent_by_type())
        print("Процент больных по видам:", self.current_service.percent_unhealthy_by_type())

    def sort_trees(self):
        trees = self.current_service.sort_by_count()
        if not trees:
            print("Список пуст.")
            return
        for tree in trees:
            print(tree)

    def save_to_csv(self):
        trees = self.current_service.get_all()
        self.csv_service.repo.save_all(trees)
        print("Данные сохранены в CSV.")

    def load_from_csv(self):
        self.current_service = self.csv_service
        self.current_name = "CSV"
        print("Загружено из CSV. Текущее хранилище: CSV.")

    def save_to_pickle(self):
        trees = self.current_service.get_all()
        self.pickle_service.repo.save_all(trees)
        print("Данные сохранены в pickle.")

    def load_from_pickle(self):
        self.current_service = self.pickle_service
        self.current_name = "pickle"
        print("Загружено из pickle. Текущее хранилище: pickle.")

    def run(self):
        while True:
            print(f"\nТекущее хранилище: {self.current_name}")
            print("""
1 - Выбрать хранилище
2 - Показать все записи
3 - Добавить запись
4 - Удалить запись
5 - Найти запись
6 - Статистика
7 - Сортировка
8 - Сохранить в CSV
9 - Загрузить из CSV
10 - Сохранить в pickle
11 - Загрузить из pickle
0 - Выход
""")
            choice = input("Выбор: ").strip()

            if choice == "0":
                print("Выход.")
                break
            elif choice == "1":
                self.choose_storage()
            elif choice == "2":
                self.read_current()
            elif choice == "3":
                self.add_tree()
            elif choice == "4":
                self.remove_tree()
            elif choice == "5":
                self.find_tree()
            elif choice == "6":
                self.show_stats()
            elif choice == "7":
                self.sort_trees()
            elif choice == "8":
                self.save_to_csv()
            elif choice == "9":
                self.load_from_csv()
            elif choice == "10":
                self.save_to_pickle()
            elif choice == "11":
                self.load_from_pickle()
            else:
                print("Неправильный ввод.")

if __name__ == "__main__":
    menu = Menu1()
    menu.run()