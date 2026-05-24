from __future__ import annotations

import math
from collections import Counter
from pathlib import Path
from statistics import mean, median, pvariance, pstdev

import matplotlib.pyplot as plt

from Task3_funk.file_hand import ExcelReportRepository, ResultFileRepository
from Task3_funk.item import ReportRes, SeriesRow, StatsRes


class ArifmService:
    """Compute ln(1 - x), save reports, analyze all stored data, and plot graphs."""

    def __init__(
        self,
        text_file: str | Path = "result_task3.txt",
        excel_file: str | Path = "result_task3.xlsx",
        graph_file: str | Path = "graph.png",
        max_iterations: int = 500,
    ):
        self.text_repo = ResultFileRepository(text_file)
        self.excel_repo = ExcelReportRepository(excel_file)
        self.graph_file = Path(graph_file)
        self.max_iterations = max_iterations

    def input_x(self) -> float:
        """Read x from the user."""
        while True:
            try:
                x = float(input("Введите x (|x| < 1): ").strip())
                if abs(x) >= 1:
                    print("Ошибка: |x| < 1")
                    continue
                return x
            except ValueError:
                print("Ошибка ввода.")

    def input_eps(self) -> float:
        """Read eps from the user."""
        while True:
            try:
                eps = float(input("Введите eps (0 < eps < 1): ").strip())
                if not (0 < eps < 1):
                    print("Ошибка: 0 < eps < 1")
                    continue
                return eps
            except ValueError:
                print("Ошибка ввода.")

    def exact(self, x: float) -> float:
        """Calculate exact function value."""
        return math.log1p(-x)

    def get_mode(self, data: list[float]) -> float | None:
        """Return the unique mode or None if there is no unique mode."""
        if not data:
            return None

        counts = Counter(data)
        max_count = max(counts.values())
        modes = [value for value, count in counts.items() if count == max_count]

        if len(modes) == 1:
            return modes[0]
        return None

    def analyze(self, values: list[float]) -> StatsRes:
        """Calculate arithmetic mean, median, mode, variance, and standard deviation."""
        return StatsRes(
            mean_value=mean(values),
            median_value=median(values),
            mode_value=self.get_mode(values),
            variance=pvariance(values),
            std_dev=pstdev(values),
        )

    def series(self, x: float, eps: float) -> tuple[float, int, list[SeriesRow], float]:
        """Compute the series for ln(1 - x)."""
        exact_value = self.exact(x)
        partial_sum = 0.0
        rows: list[SeriesRow] = []

        for n in range(1, self.max_iterations + 1):
            term = -(x ** n) / n
            partial_sum += term
            abs_error = abs(exact_value - partial_sum)

            rows.append(SeriesRow(
                n=n,
                term=term,
                partial_sum=partial_sum,
                abs_error=abs_error
            ))

            if abs_error <= eps:
                return partial_sum, n, rows, exact_value

        print(f"Предупреждение: достигнут предел {self.max_iterations} итераций.")
        return partial_sum, self.max_iterations, rows, exact_value

    def build_report(self, x: float, eps: float) -> ReportRes:
        """Build a complete report object."""
        approx_value, iterations, rows, exact_value = self.series(x, eps)
        stats = self.analyze([row.partial_sum for row in rows])

        return ReportRes(
            x=x,
            eps=eps,
            exact_value=exact_value,
            approx_value=approx_value,
            iterations=iterations,
            rows=rows,
            stats=stats,
        )

    def plot(self, report: ReportRes, number: int) -> None:
        """Plot the series and exact function on one axis, then save and show it."""
        n_values = [row.n for row in report.rows]
        series_values = [row.partial_sum for row in report.rows]
        exact_values = [report.exact_value for _ in report.rows]

        plt.figure(figsize=(10, 6))
        plt.plot(n_values, series_values, marker="o", linewidth=2, label="Ряд")
        plt.plot(n_values, exact_values, linewidth=2, label="Math F(x)")

        plt.axhline(0, linewidth=1)
        plt.axvline(0, linewidth=1)
        plt.xlabel("n")
        plt.ylabel("F(x)")
        plt.title("Разложение ln(1 - x) в ряд")
        plt.grid(True)
        plt.legend()

        plt.text(
            0.02,
            0.02,
            f"x = {report.x}\neps = {report.eps}\niterations = {report.iterations}",
            transform=plt.gca().transAxes,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
        )

        if report.rows:
            last = report.rows[-1]
            plt.annotate(
                f"{last.partial_sum:.6f}",
                xy=(last.n, last.partial_sum),
                xytext=(last.n, last.partial_sum + 0.05),
                arrowprops=dict(arrowstyle="->")
            )

        plt.tight_layout()
        self.graph_file = Path(f"{number}_graph.png")
        plt.savefig(self.graph_file, dpi=300)
        plt.show()

    def calculate_and_save(self) -> None:
        """Calculate one report, append it to files, and show the graph."""
        x = self.input_x()
        eps = self.input_eps()

        report = self.build_report(x, eps)

        self.text_repo.append_report(report)
        self.excel_repo.append_report(report)

        # print("\nРезультат:")
        # print(f"x = {report.x}")
        # print(f"eps = {report.eps}")
        # print(f"n = {report.iterations}")
        # print(f"F(x) = {report.approx_value:.12f}")
        # print(f"Math F(x) = {report.exact_value:.12f}")
        # print("Результат дописан в файл.")
        # print("Excel-таблица обновлена.")

        # self.plot(report)

    def analyze_all_reports(self) -> None:
        """Read all saved reports and analyze each one separately."""
        reports = self.text_repo.read_all_reports()
        if not reports:
            print("Файл пуст или ещё не создан.")
            return

        stripe = "=" * 90
        print("\nАНАЛИЗ ВСЕХ РАСЧЁТОВ")
        print(stripe)

        for idx, report in enumerate(reports, start=1):
            seq_values = [row.partial_sum for row in report.rows]
            stats = self.analyze(seq_values)

            print(f"\nРасчёт №{idx}")
            print(f"x = {report.x}")
            print(f"eps = {report.eps}")
            print(f"n = {report.iterations}")
            print(f"F(x) = {report.approx_value:.12f}")
            print(f"Math F(x) = {report.exact_value:.12f}")
            print(f"Среднее арифметическое = {stats.mean_value:.12f}")
            print(f"Медиана = {stats.median_value:.12f}")
            print(f"Мода = {stats.mode_value}")
            print(f"Дисперсия = {stats.variance:.12f}")
            print(f"СКО = {stats.std_dev:.12f}")

        print(stripe)

    def export_excel_plot(self) -> None:
        """Rebuild Excel workbook from all saved reports and plot graf."""
        reports = self.text_repo.read_all_reports()
        if not reports:
            print("Нет данных для экспорта.")
            return
        for i, report in enumerate(reports):
            self.plot(report, i)
        self.excel_repo.export_all(reports)
        print("Excel-файл пересоздан по всем данным из текстового файла.")