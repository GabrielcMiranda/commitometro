from __future__ import annotations

import re
from dataclasses import dataclass

from . import ExpressaoRegular, REGISTRO

PADRAO_REFERENCIA = (
    r"([Cc]lose[sd]?|[Ff]ix(es|ed)?|[Rr]esolve[sd]?|[Rr]efs):? "
    r"([a-z0-9-]+/[a-z0-9._-]+)?#[1-9][0-9]*"
    r"(, ([a-z0-9-]+/[a-z0-9._-]+)?#[1-9][0-9]*)*"
)

REGISTRO["ER-05"] = ExpressaoRegular(
    id="ER-05",
    nome="Referência a issue",
    finalidade=(
        "Encontrar linhas que fecham ou referenciam issues (palavras-chave do GitHub), "
        "inclusive de outro repositório."
    ),
    alfabeto=(
        "K = (C|c)lose(s|d|ε) | (F|f)ix(es|ed|ε) | (R|r)esolve(s|d|ε) | (R|r)efs; "
        "O = {a,…,z} ∪ {0,…,9} ∪ {-}; R = O ∪ {., _}; D, P como na ER-03; "
        "I = ( O O* / R R* | ε ) # P D*."
    ),
    linguagem=(
        "Uma palavra-chave de fechamento ou referência, um separador opcional, e uma "
        "lista de uma ou mais issues separadas por vírgula e espaço."
    ),
    formal="K ( : | ε ) ␣ I ( ,␣ I )*",
    padrao=PADRAO_REFERENCIA,
    grupos={1: "palavra-chave"},
)

_PALAVRAS_FECHAM = {
    "close", "closes", "closed",
    "fix", "fixes", "fixed",
    "resolve", "resolves", "resolved",
}


@dataclass(frozen=True, slots=True)
class Referencia:
    palavra_chave: str
    fecha: bool
    issues: tuple[str, ...]


def validar_referencia(linha: str) -> Referencia | None:
    correspondencia = re.fullmatch(PADRAO_REFERENCIA, linha)
    if correspondencia is None:
        return None
    palavra_chave = correspondencia.group(1)
    resto = linha[correspondencia.end(1):].lstrip(":").lstrip(" ")
    issues = tuple(resto.split(", "))
    return Referencia(
        palavra_chave=palavra_chave,
        fecha=palavra_chave.lower() in _PALAVRAS_FECHAM,
        issues=issues,
    )
