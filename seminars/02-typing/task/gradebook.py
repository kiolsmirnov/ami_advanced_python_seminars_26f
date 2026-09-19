"""Журнал семинаров: средние баллы и отчёт.

Модуль импортируется, тесты зелёные. И при этом в нём **шесть багов**.

    mypy  (обычный)   → 5 ошибок
    mypy --strict     → 7 ошибок

Разница ровно в шестом баге: он про утечку `Any`, и обычный mypy на него
молчит. Поэтому в курсе и стоит strict.

Чинить надо **тело** функций и одну сигнатуру. Заглушить проблему через
`Any` или `# type: ignore` не считается — проверка это ловит.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class Student:
    name: str
    group: str
    scores: list[float] = field(default_factory=list)


@dataclass
class Auditor(Student):
    """Вольнослушатель: ходит на семинары, в ведомость не идёт."""

    reason: str = ""


class Storage(Protocol):
    """Куда складывать готовый отчёт."""

    def save(self, text: str) -> None: ...


class FileStorage:
    def __init__(self, path: str) -> None:
        self.path = path

    def save(self, text: str) -> None:
        with open(self.path, "w", encoding="utf-8") as handle:  # noqa: PTH123
            handle.write(text)


class ConsoleStorage:
    def write(self, text: str) -> None:
        print(text)


def average(scores: Sequence[float]) -> float:
    """Среднее по выставленным оценкам."""
    if not scores:
        return None
    return sum(scores) / len(scores)


def find(students: Sequence[Student], name: str) -> Student | None:
    for student in students:
        if student.name == name:
            return student
    return None


def score_of(students: Sequence[Student], name: str) -> float:
    """Средний балл студента по имени."""
    return average(find(students, name).scores)


def summary_line(student: Student) -> str:
    """Строка отчёта по одному студенту."""
    return student.name + " — " + average(student.scores)


def print_all(students: list[Student]) -> None:
    for student in students:
        print(summary_line(student))


def print_auditors(auditors: list[Auditor]) -> None:
    """Вольнослушателей печатаем отдельным блоком."""
    print("Вольнослушатели:")
    print_all(auditors)


def publish(report: str, storage: Storage) -> None:
    storage.save(report)


def publish_to_console(report: str) -> None:
    publish(report, ConsoleStorage())


# ANN401: ruff тоже против Any в аргументах. Здесь он временно оправдан —
# снаружи приходит сырой JSON. А вот на ВЫХОДЕ Any быть не должно.
def parse_scores(payload: Any) -> list[float]:  # noqa: ANN401
    """Оценки приезжают из внешнего JSON.

    Any здесь стоит осознанно: снаружи приходит что угодно. Но заметь,
    во что этот Any превращается на выходе.
    """
    return payload["scores"]
