'''
Задание 5. В соответствии с заданием своего варианта исследовать возможности библиотека NumPy при работе с массивами и математическими и статическими операциями. 
Сформировать целочисленную матрицу А[n,m] с помощью генератора случайных чисел (random).
а) Библиотека NumPy.
1. Создание массива. Функции array() и values().
2. Функции создания массива заданного вида.
3. Индексирование массивов NumPy. Индекс и срез.
4. Операции с массивами. Универсальные (поэлементные) функции.

б) Математические и статистические операции.
1. Функция mean()
2. Функция median()
3. Функция corrcoef()
4. Дисперсия var().
5. Стандартное отклонение std()

Вычислить сумму элементов матрицы, расположенных ниже главной диагонали.
Вычислить стандартное отклонение для элементов главной диагонали
матрицы. Ответ округлите до сотых. Вычисление стандартного отклонения
выполнить двумя способами: через стандартную функцию и через
программирование формулы
'''
from __future__ import annotations
from Task2_funk.text_repository import TextRepository
from Task2_funk.text_service import TextService


from Task5_funk.numpy_service import NumPyMatrixService


class Menu5:
    """Console menu for Task 5."""

    def __init__(self):
        self.service = NumPyMatrixService()

    def run(self) -> None:
        """Run the main menu loop."""
        while True:
            print(
                """
================ МЕНЮ ================
1 - Создать матрицу и выполнить расчёты
2 - Показать текущую матрицу
3 - Показать операции NumPy
4 - Дописать результат в файл
5 - Показать все сохранённые расчёты
0 - Выход
"""
            )
            choice = input("Выбор: ").strip()

            if choice == "0":
                print("Выход.")
                break
            elif choice == "1":
                report = self.service.create_and_analyze_matrix()
                print("\nМатрица создана.")
                print(f"Сумма элементов ниже главной диагонали: {report.below_diag_sum}")
                print(f"СКО главной диагонали (NumPy): {report.stats.std_main_diag_numpy:.2f}")
                print(f"СКО главной диагонали (формула): {report.stats.std_main_diag_formula:.2f}")
            elif choice == "2":
                self.service.show_current_matrix()
            elif choice == "3":
                self.service.show_numpy_demo()
            elif choice == "4":
                self.service.save_current_report()
            elif choice == "5":
                reports = self.service.repo.read_all_reports()
                if not reports:
                    print("Файл пуст.")
                else:
                    print("\nСохранённые расчёты:")
                    for idx, rep in enumerate(reports, start=1):
                        print(f"\nРасчёт №{idx}")
                        print(f"n = {rep.n}, m = {rep.m}")
                        print(f"Границы: [{rep.low}, {rep.high}]")
                        print(f"Сумма ниже диагонали: {rep.below_diag_sum}")
                        print(f"Mean main diag: {rep.stats.mean_main_diag:.2f}")
                        print(f"Median main diag: {rep.stats.median_main_diag:.2f}")
                        print(f"Variance: {rep.stats.variance_main_diag:.2f}")
                        print(f"Std NumPy: {rep.stats.std_main_diag_numpy:.2f}")
                        print(f"Std Formula: {rep.stats.std_main_diag_formula:.2f}")
                        print(f"Corrcoef: {rep.stats.corrcoef_diag}")
            else:
                print("Неверный ввод.")

if __name__ == "__main__":
    menu = Menu5()
    menu.run()