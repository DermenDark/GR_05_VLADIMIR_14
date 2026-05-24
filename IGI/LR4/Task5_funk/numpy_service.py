from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from Task5_funk.file_hand import MatrixReportRepository
from Task5_funk.item import MatrixReportRes, MatrixStatsRes


class NumPyMatrixService:
    """Generate, analyze, store, and display NumPy matrices."""

    def __init__(self, file_path: str | Path = "result_task5.txt"):
        self.repo = MatrixReportRepository(file_path)
        self.current_matrix: np.ndarray | None = None
        self.current_report: MatrixReportRes | None = None

    def input_int(self, prompt: str, min_value: int | None = None) -> int:
        """Read an integer from the user."""
        while True:
            try:
                value = int(input(prompt).strip())
                if min_value is not None and value < min_value:
                    print(f"Ошибка: значение должно быть не меньше {min_value}.")
                    continue
                return value
            except ValueError:
                print("Ошибка ввода. Введите целое число.")

    def input_bounds(self) -> tuple[int, int]:
        """Read matrix element bounds."""
        while True:
            try:
                low = int(input("Введите нижнюю границу случайных чисел: ").strip())
                high = int(input("Введите верхнюю границу случайных чисел: ").strip())
                if low > high:
                    print("Ошибка: нижняя граница не может быть больше верхней.")
                    continue
                return low, high
            except ValueError:
                print("Ошибка ввода. Введите целые числа.")

    def generate_matrix(self, n: int, m: int, low: int, high: int) -> np.ndarray:
        """Generate an integer matrix with random values."""
        return np.random.randint(low, high + 1, size=(n, m), dtype=int)

    def below_main_diagonal_sum(self, matrix: np.ndarray) -> int:
        """Calculate the sum of elements below the main diagonal."""
        return int(np.tril(matrix, k=-1).sum())

    def main_diagonal(self, matrix: np.ndarray) -> np.ndarray:
        """Return the main diagonal of the matrix."""
        return np.diag(matrix)

    def secondary_diagonal(self, matrix: np.ndarray) -> np.ndarray:
        """Return the secondary diagonal of the matrix."""
        return np.fliplr(matrix).diagonal()

    def std_numpy(self, diag: np.ndarray) -> float:
        """Calculate standard deviation with NumPy."""
        return float(np.std(diag))

    def std_formula(self, diag: np.ndarray) -> float:
        """Calculate standard deviation using a formula."""
        mean_value = float(np.mean(diag))
        variance = float(np.sum((diag - mean_value) ** 2) / diag.size)
        return float(np.sqrt(variance))

    def build_stats(self, matrix: np.ndarray) -> MatrixStatsRes:
        """Build statistics for the matrix diagonal."""
        main_diag = self.main_diagonal(matrix)
        sec_diag = self.secondary_diagonal(matrix)

        corrcoef_value: float | None = None
        if main_diag.size == sec_diag.size and main_diag.size > 1:
            corrcoef_value = float(np.corrcoef(main_diag, sec_diag)[0, 1])

        return MatrixStatsRes(
            mean_main_diag=float(np.mean(main_diag)),
            median_main_diag=float(np.median(main_diag)),
            corrcoef_diag=corrcoef_value,
            variance_main_diag=float(np.var(main_diag)),
            std_main_diag_numpy=self.std_numpy(main_diag),
            std_main_diag_formula=self.std_formula(main_diag),
        )

    def build_report(self, matrix: np.ndarray, n: int, m: int, low: int, high: int) -> MatrixReportRes:
        """Build a full report for the matrix."""
        stats = self.build_stats(matrix)
        below_sum = self.below_main_diagonal_sum(matrix)

        return MatrixReportRes(
            n=n,
            m=m,
            low=low,
            high=high,
            matrix=matrix.tolist(),
            below_diag_sum=below_sum,
            stats=stats,
        )

    def create_and_analyze_matrix(self) -> MatrixReportRes:
        """Create a new matrix and analyze it."""
        n = self.input_int("Введите n (строки): ", min_value=1)
        m = self.input_int("Введите m (столбцы): ", min_value=1)
        low, high = self.input_bounds()

        matrix = self.generate_matrix(n, m, low, high)
        report = self.build_report(matrix, n, m, low, high)

        self.current_matrix = matrix
        self.current_report = report
        return report

    def save_current_report(self) -> None:
        """Append current report to file."""
        if self.current_report is None:
            print("Сначала создайте матрицу.")
            return

        self.repo.append_report(self.current_report)
        print("Результат дописан в файл.")

    def show_current_matrix(self) -> None:
        """Print the current matrix."""
        if self.current_matrix is None:
            print("Матрица ещё не создана.")
            return

        print("\nТекущая матрица:")
        print(self.current_matrix)

    def show_numpy_demo(self) -> None:
        """Show basic NumPy operations requested in the assignment."""
        if self.current_matrix is None:
            print("Сначала создайте матрицу.")
            return

        a = self.current_matrix
        print("\n1) Создание массива:")
        print("array():")
        print(np.array(a.tolist()))

        print("\n2) Функции создания массива заданного вида:")
        print("zeros:")
        print(np.zeros_like(a))
        print("ones:")
        print(np.ones_like(a))
        print("eye:")
        print(np.eye(min(a.shape), dtype=int))

        print("\n3) Индексирование и срез:")
        print("a[0, 0] =", a[0, 0])
        print("a[0] =", a[0])
        print("a[:, 0] =", a[:, 0])

        print("\n4) Универсальные функции:")
        print("abs(a):")
        print(np.abs(a))
        print("square(a):")
        print(np.square(a))
        print("sqrt(abs(a)):")
        print(np.sqrt(np.abs(a)))

        print("\n5) Математические и статистические операции:")
        print("mean =", float(np.mean(a)))
        print("median =", float(np.median(a)))
        print("var =", float(np.var(a)))
        print("std =", float(np.std(a)))
        print("corrcoef(main, secondary) =")
        main_diag = self.main_diagonal(a)
        sec_diag = self.secondary_diagonal(a)
        if main_diag.size == sec_diag.size and main_diag.size > 1:
            print(np.corrcoef(main_diag, sec_diag))
        else:
            print("Недостаточно данных для corrcoef.")