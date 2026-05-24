from Task1 import Menu1
from Task2 import Menu2
from Task3 import Menu3
from Task4 import Menu4
from Task5 import Menu5
from Task6 import Menu6


class MasterMenu:
    """Main menu for switching between tasks."""

    def __init__(self):
        self.menus = {
            "1": ("Задание 1", Menu1),
            "2": ("Задание 2", Menu2),
            "3": ("Задание 3", Menu3),
            "4": ("Задание 4", Menu4),
            "5": ("Задание 5", Menu5),
            "6": ("Задание 6", Menu6),
        }

    def show_menu(self):
        """Display the main menu."""
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        for key, (title, _) in self.menus.items():
            print(f"{key} - {title}")
        print("0 - Выход")

    def run(self):
        """Run the main menu loop."""
        while True:
            self.show_menu()
            choice = input("Выбор: ").strip()

            if choice == "0":
                print("Выход.")
                break

            if choice in self.menus:
                title, menu_cls = self.menus[choice]
                print(f"\nОткрывается: {title}")
                menu = menu_cls()
                menu.run()
            else:
                print("Неверный ввод.")


if __name__ == "__main__":
    MasterMenu().run()