from __future__ import annotations

"""Улучшенная ООП-версия (ВСЕ задания работают с датасетом)

Изменения:
- ВСЕ операции (Series, DataFrame, loc/iloc) выполняются на реальном датасете
- Более логичная структура
- Чёткое разделение логики
"""

from pathlib import Path
from typing import Optional

import pandas as pd

try:
    from IPython.display import display
except Exception:
    def display(obj):
        print(obj)


# ======================
# DATA LAYER
# ======================
class DatasetManager:
    DATASET_ID = "dansbecker/melbourne-housing-snapshot"

    def __init__(self):
        self._df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        if self._df is not None:
            return self._df

        import kagglehub

        path = Path(kagglehub.dataset_download(self.DATASET_ID))
        csv_files = list(path.rglob("*.csv"))

        if not csv_files:
            raise FileNotFoundError("CSV файл не найден")

        self._df = pd.read_csv(csv_files[0])
        return self._df

class PandasService:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # 1
    def show_import(self):
        print("Pandas version:", pd.__version__)

    # 2
    def show_series(self):
        s = self.df["Price"].head(10)
        print("Series (Price):")
        display(s)

    # 3
    def show_display(self):
        print("DataFrame preview:")
        display(self.df.head())

    # 4
    def loc_iloc(self):
        print("loc[0]:")
        display(self.df.loc[0])

        print("iloc[0]:")
        display(self.df.iloc[0])

    # 5
    def show_dataframe(self):
        display(self.df.head(10))

    # 6/7
    def info(self):
        print(self.df.info())
        display(self.df.describe())

    # 8
    def multiindex(self):
        df = self.df.dropna(subset=["Rooms", "Type", "Price"])
        df = df[df["Rooms"] > 0]

        s = df.set_index(["Rooms", "Type"])["Price"]
        s.index.set_names(["Rooms", "Type"], inplace=True)

        print("MultiIndex Series:")
        display(s.head(20))
        return s

    # 9
    def ratio(self):
        df = self.df.dropna(subset=["Rooms", "Price"])
        df = df[df["Rooms"] > 0]

        max_r = df["Rooms"].max()
        min_r = df["Rooms"].min()

        avg_max = df[df["Rooms"] == max_r]["Price"].mean()
        avg_min = df[df["Rooms"] == min_r]["Price"].mean()

        result = round(avg_max / avg_min, 2)
        print("Ответ:", result)
        return result
