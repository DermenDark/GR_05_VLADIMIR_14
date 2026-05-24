from typing import Optional
import pandas as pd
from Task6_funk.base_funk import DatasetManager, PandasService
try:
    from IPython.display import display
except Exception:
    def display(obj):
        print(obj)

class Menu6:
    def __init__(self):
        self.dataset = DatasetManager()
        self.df: Optional[pd.DataFrame] = None

    def run(self):
        while True:
            print("""
1 - import pandas
2 - Series (из датасета)
3 - display DataFrame
4 - loc / iloc
5 - DataFrame preview
6 - загрузить датасет
7 - info + describe
8 - MultiIndex
9 - ratio
0 - exit
""")

            choice = input("Выбор: ")

            try:
                if choice == "6":
                    self.df = self.dataset.load()
                    print("Датасет загружен")
                    continue

                self._ensure_df()
                service = PandasService(self.df)

                if choice == "1":
                    service.show_import()

                elif choice == "2":
                    service.show_series()

                elif choice == "3":
                    service.show_display()

                elif choice == "4":
                    service.loc_iloc()

                elif choice == "5":
                    service.show_dataframe()

                elif choice == "7":
                    service.info()

                elif choice == "8":
                    service.multiindex()

                elif choice == "9":
                    service.ratio()

                elif choice == "0":
                    break

            except Exception as e:
                print("Ошибка:", e)

    def _ensure_df(self):
        if self.df is None:
            self.df = self.dataset.load()
