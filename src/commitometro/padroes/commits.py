from __future__ import annotations

import re
from dataclasses import dataclass

from . import ExpressaoRegular, REGISTRO

PADRAO_CABECALHO = (
    r"(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\(([a-z0-9]+(-[a-z0-9]+)*)\))?(!?): ([^ \n][^\n]*)"
)

PADRAO_RODAPE = r"(BREAKING CHANGE|[A-Za-z]+(-[A-Za-z]+)*)(: | #)([^ \n][^\n]*)"

_TOKENS_QUEBRA = {"BREAKING CHANGE", "BREAKING-CHANGE"}


@dataclass(frozen=True, slots=True)
class Cabecalho:
    tipo: str
    escopo: str | None
    quebra: bool
    descricao: str


@dataclass(frozen=True, slots=True)
class Rodape:
    token: str
    separador: str
    valor: str
    quebra: bool


def validar_cabecalho(linha: str) -> Cabecalho | None:
    correspondencia = re.fullmatch(PADRAO_CABECALHO, linha)
    if correspondencia is None:
        return None
    tipo, _, escopo, _, marca, descricao = correspondencia.groups()
    return Cabecalho(tipo=tipo, escopo=escopo, quebra=marca == "!", descricao=descricao)


def validar_rodape(linha: str) -> Rodape | None:
    correspondencia = re.fullmatch(PADRAO_RODAPE, linha)
    if correspondencia is None:
        return None
    token, _, separador, valor = correspondencia.groups()
    return Rodape(token=token, separador=separador, valor=valor, quebra=token in _TOKENS_QUEBRA)


REGISTRO["ER-01"] = ExpressaoRegular(
    id="ER-01",
    nome="Cabeçalho de commit (Conventional Commits)",
    finalidade=(
        "Validar a 1ª linha do commit no formato tipo(escopo)!: descrição e extrair "
        "tipo, escopo e marca de quebra."
    ),
    alfabeto=(
        "Σ = caracteres Unicode; T = feat | fix | docs | style | refactor | perf | test | "
        "build | ci | chore | revert; A = {a,…,z} ∪ {0,…,9}; C = Σ − {\\n}; C₀ = C − {␣}."
    ),
    linguagem=(
        "Um tipo de T, opcionalmente um escopo entre parênteses formado por palavras de A "
        "separadas por hífen simples, opcionalmente !, depois : e um espaço, e uma "
        "descrição não vazia que não começa com espaço."
    ),
    formal="T ( '(' A A* ( - A A* )* ')' | ε ) ( ! | ε ) :␣ C₀ C*",
    padrao=PADRAO_CABECALHO,
    grupos={1: "tipo", 3: "escopo", 5: "marca de quebra (! ou vazio)", 6: "descrição"},
)

REGISTRO["ER-02"] = ExpressaoRegular(
    id="ER-02",
    nome="Linha de rodapé (trailer)",
    finalidade=(
        "Reconhecer linhas de rodapé do Conventional Commits/git trailers e detectar "
        "BREAKING CHANGE."
    ),
    alfabeto="L = {A,…,Z} ∪ {a,…,z}; W = L L*; C e C₀ como na ER-01.",
    linguagem=(
        "Um token (BREAKING CHANGE ou palavras de letras unidas por hífen), seguido do "
        "separador ': ' ou ' #', e de um valor não vazio que não começa com espaço."
    ),
    formal="( BREAKING␣CHANGE | W ( - W )* ) ( :␣ | ␣# ) C₀ C*",
    padrao=PADRAO_RODAPE,
    grupos={1: "token", 3: "separador", 4: "valor"},
)
