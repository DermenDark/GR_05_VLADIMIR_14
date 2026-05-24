from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import zipfile

from Task2_funk.text_repository import TextRepository


WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)*")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]*", re.DOTALL)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
SMILEY_RE = re.compile(r'(?::|;)-*([()\[\]])\1*')


VOWELS = set("аеёиоуыэюяaeiouy")
RUS_CONSONANTS = set("бвгджзйклмнпрстфхцчшщ")
LAT_CONSONANTS = set("bcdfghjklmnpqrstvwxyz")


@dataclass(slots=True)
class TextAnalysisResult:
    """Store all calculated metrics and extracted lists."""

    total_sentences: int
    declarative_sentences: int
    interrogative_sentences: int
    imperative_sentences: int
    average_sentence_length: float
    average_word_length: float
    smiley_count: int
    years: list[str]
    special_words: list[str]
    words_starting_with_vowel: int
    doubled_letter_words: list[tuple[int, str]]
    alphabetic_words: list[str]


class TextService:
    """Analyze text with regular expressions and build a report."""

    def __init__(self, repository: TextRepository):
        self.repository = repository

    def get_text(self) -> str:
        """Load the input text from the repository."""
        return self.repository.read_text()

    def extract_words(self, text: str) -> list[str]:
        """Extract all words from the text."""
        return WORD_RE.findall(text)

    def split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        parts = [part.strip() for part in SENTENCE_RE.findall(text)]
        return [part for part in parts if part]

    def count_sentence_types(self, sentences: Iterable[str]) -> tuple[int, int, int]:
        """Count declarative, interrogative, and imperative sentences."""
        declarative = interrogative = imperative = 0

        for sentence in sentences:
            stripped = sentence.strip()
            if stripped.endswith("."):
                declarative += 1
            elif stripped.endswith("?"):
                interrogative += 1
            elif stripped.endswith("!"):
                imperative += 1

        return declarative, interrogative, imperative

    def average_sentence_length(self, text: str, sentence_count: int) -> float:
        """Compute average sentence length in characters using words only."""
        if sentence_count == 0:
            return 0.0
        words = self.extract_words(text)
        total_chars = sum(len(word) for word in words)
        return total_chars / sentence_count

    def average_word_length(self, text: str) -> float:
        """Compute average word length in characters."""
        words = self.extract_words(text)
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)

    def count_smileys(self, text: str) -> int:
        """Count emoticons that satisfy the given pattern."""
        return len(SMILEY_RE.findall(text))

    def extract_years(self, text: str) -> list[str]:
        """Extract all four-digit years from the text."""
        return YEAR_RE.findall(text)

    def words_with_third_from_end_consonant_and_penultimate_vowel(self, text: str) -> list[str]:
        """Find words whose third-from-end letter is consonant and penultimate letter is vowel."""
        result: list[str] = []
        for word in self.extract_words(text):
            low = word.lower()
            if len(low) < 3:
                continue
            third_from_end = low[-3]
            penultimate = low[-2]
            if self._is_consonant(third_from_end) and self._is_vowel(penultimate):
                result.append(word)
        return result

    def count_words_starting_with_vowel(self, text: str) -> int:
        """Count words that start with a vowel."""
        words = self.extract_words(text)
        return sum(1 for word in words if word and self._is_vowel(word[0].lower()))

    def words_with_double_letters(self, text: str) -> list[tuple[int, str]]:
        """Find words that contain a doubled letter and return their ordinal numbers."""
        result: list[tuple[int, str]] = []
        for index, word in enumerate(self.extract_words(text), start=1):
            low = word.lower()
            if re.search(r"(.)\1", low):
                result.append((index, word))
        return result

    def alphabetic_words(self, text: str) -> list[str]:
        """Return all words sorted alphabetically."""
        words = self.extract_words(text)
        return sorted(words, key=lambda item: item.lower())

    def analyze(self) -> TextAnalysisResult:
        """Analyze the full text and return a structured result object."""
        text = self.get_text()
        sentences = self.split_sentences(text)
        decl, quest, imp = self.count_sentence_types(sentences)
        words = self.extract_words(text)

        return TextAnalysisResult(
            total_sentences=len(sentences),
            declarative_sentences=decl,
            interrogative_sentences=quest,
            imperative_sentences=imp,
            average_sentence_length=self.average_sentence_length(text, len(sentences)),
            average_word_length=self.average_word_length(text),
            smiley_count=self.count_smileys(text),
            years=self.extract_years(text),
            special_words=self.words_with_third_from_end_consonant_and_penultimate_vowel(text),
            words_starting_with_vowel=self.count_words_starting_with_vowel(text),
            doubled_letter_words=self.words_with_double_letters(text),
            alphabetic_words=sorted(words, key=lambda item: item.lower()),
        )

    def build_report(self, result: TextAnalysisResult) -> str:
        """Build a human-readable report from the analysis result."""
        
        lines = [
            "ОТЧЁТ ОБ АНАЛИЗЕ ТЕКСТА",
            "=" * 80,
            f"Общее количество предложений: {result.total_sentences}",
            f"Повествовательные предложения: {result.declarative_sentences}",
            f"Вопросительные предложения: {result.interrogative_sentences}",
            f"Побудительные предложения: {result.imperative_sentences}",
            f"Средняя длина предложения (только слова): {result.average_sentence_length:.2f}",
            f"Средняя длина слова: {result.average_word_length:.2f}",
            f"Количество смайликов: {result.smiley_count}",
            "",
            "Годы / даты:",
            ", ".join(result.years) if result.years else "Нет",
            "",
            "Слова, у которых третья с конца буква согласная, а предпоследняя — гласная:",
            ", ".join(result.special_words) if result.special_words else "Нет",
            "",
            f"Количество слов, начинающихся с гласной: {result.words_starting_with_vowel}",
            "",
            "Слова с двумя одинаковыми буквами подряд и их порядковые номера:",
        ]

        if result.doubled_letter_words:
            lines.extend(f"{index}: {word}" for index, word in result.doubled_letter_words)
        else:
            lines.append("None")

        lines.extend(
            [
                "",
                "Слова в алфавитном порядке:",
                ", ".join(result.alphabetic_words) if result.alphabetic_words else "None",
                "=" * 80,
            ]
        )
        return "\n".join(lines)

    def save_report(self, report: str) -> None:
        """Save the report to the result file."""
        self.repository.write_result(report)

    def create_zip_archive(self, zip_path: str | Path) -> dict[str, int | str]:
        """Create a ZIP archive with the result file and return archive metadata."""
        zip_path = Path(zip_path)
        with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(self.repository.result_path, arcname=self.repository.result_path.name)

        with zipfile.ZipFile(zip_path, mode="r") as archive:
            info = archive.getinfo(self.repository.result_path.name)
            return {
                "archive_name": zip_path.name,
                "file_name": info.filename,
                "compressed_size": info.compress_size,
                "original_size": info.file_size,
            }

    def analyze_and_save(self, zip_path: str | Path) -> tuple[TextAnalysisResult, str, dict[str, int | str]]:
        """Run the full pipeline: analyze text, save report, and zip the result."""
        result = self.analyze()
        report = self.build_report(result)
        self.save_report(report)
        archive_info = self.create_zip_archive(zip_path)
        return result, report, archive_info

    def _is_vowel(self, ch: str) -> bool:
        """Check whether a character is a vowel."""
        return ch in VOWELS

    def _is_consonant(self, ch: str) -> bool:
        """Check whether a character is a consonant."""
        return ch in RUS_CONSONANTS or ch in LAT_CONSONANTS