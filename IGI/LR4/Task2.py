'''
Задание 2.Считать из исходного файла текст.
    Используя регулярные выражения получить искомую информацию (см. условие),
    вывести ее на экран и сохранить в другой файл. Заархивировать файл с результатом
    с помощью модуля zipfile и обеспечить получение информации о файле в архиве.
    
    Также выполнить общее задание – определить и сохранить в файл с результатами:
        –количество предложений в тексте;
        –количество предложений в тексте каждого вида отдельно
        (повествовательные, вопросительные и побудительные);
        –среднюю длину предложения в символах (считаются только слова);
        –среднюю длину слова в тексте в символах;
        –количество смайликов в заданном тексте.
        Смайликом будем считать последовательность символов, удовлетворяющую условиям:
            первым символом является либо «;» (точка с запятой) либо «:» (двоеточие) ровно один раз;
            далее может идти символ «-» (минус) сколько угодно раз (в том числе символ минус может идти ноль раз);
            в конце обязательно идет некоторое количество (не меньше одной) одинаковых скобок из следующего набора: «(», «)», «[», «]»;
            внутри смайлика не может встречаться никаких других символов.
            Например, эта последовательность является смайликом: «;---------[[[[[[[[».
            Эти последовательности смайликами не являются: «]», «;--»,«:»,«)».

        Получить список дат (формат 2007)
    Из заданной строки получить список слов,
    у которых третья с конца буква согласная, а предпоследняя – гласная.
    определить число слов в строке, начинающихся с гласной;
    найти слова, содержащие две одинаковые буквы подряд и их
    порядковые номера;
    вывести слова в алфавитном порядке
'''
from __future__ import annotations
from pathlib import Path
from Task2_funk.text_repository import TextRepository
from Task2_funk.text_service import TextService


class Menu2:
    """Provide a console menu for text analysis tasks."""

    def __init__(self):
        self.input_path = Path("input.txt")
        self.result_path = Path("result_task2.txt")
        self.archive_path = Path("result_task2.zip")
        self.repository = TextRepository(self.input_path, self.result_path)
        self.service = TextService(self.repository)

    def show_report(self):
        """Analyze the input text and print the report."""
        try:
            _, report, archive_info = self.service.analyze_and_save(self.archive_path)
        except FileNotFoundError:
            print("Input file not found. Create input.txt first.")
            return

        print(report)
        print("\nArchive info:")
        for key, value in archive_info.items():
            print(f"{key}: {value}")

    def show_raw_text(self):
        """Print the raw source text."""
        try:
            print(self.repository.read_text())
        except FileNotFoundError:
            print("Input file not found. Create input.txt first.")

    def run(self):
        """Run the menu loop."""
        while True:
            # print("\nCurrent files:")
            # print(f"Input:  {self.input_path}")
            # print(f"Result: {self.result_path}")
            # print(f"Zip:    {self.archive_path}")
            print(
                """
1 - Показать исходник
2 - Анализировать текст и показать результат
0 - Выход
"""
            )
            choice = input("Выбор: ").strip()

            if choice == "0":
                print("Выход.")
                break
            elif choice == "1":
                self.show_raw_text()
            elif choice == "2":
                self.show_report()
            else:
                print("неправильный ввод.")

if __name__ == "__main__":
    menu = Menu2()
    menu.run()