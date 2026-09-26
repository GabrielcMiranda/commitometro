from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ExpressaoRegular:
    id: str
    nome: str
    finalidade: str
    alfabeto: str
    linguagem: str
    formal: str
    padrao: str
    grupos: dict[int, str] = field(default_factory=dict)

    @property
    def compilada(self) -> re.Pattern[str]:
        return re.compile(self.padrao)


REGISTRO: dict[str, ExpressaoRegular] = {}

from . import commits
