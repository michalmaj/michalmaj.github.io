from dataclasses import dataclass
from typing import Literal

Level = Literal["error", "warning"]


@dataclass(frozen=True)
class Issue:
    level: Level
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper()} [{self.code}] {self.path}: {self.message}"


def error(code: str, path: str, message: str) -> Issue:
    return Issue("error", code, path, message)


def warning(code: str, path: str, message: str) -> Issue:
    return Issue("warning", code, path, message)
