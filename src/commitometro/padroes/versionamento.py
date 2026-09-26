from __future__ import annotations

import re
from dataclasses import dataclass

from . import ExpressaoRegular, REGISTRO

PADRAO_VERSAO = (
    r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(-(alpha|beta|rc)(\.(0|[1-9][0-9]*))?)?"
)

REGISTRO["ER-03"] = ExpressaoRegular(
    id="ER-03",
    nome="Tag de versão semântica",
    finalidade=(
        "Reconhecer tags SemVer, com ou sem v e com pré-lançamento opcional, para "
        "ordenar versões e sugerir a próxima."
    ),
    alfabeto="D = {0,…,9}; P = D − {0}; N = 0 | P D* (número sem zero à esquerda).",
    linguagem=(
        "Um prefixo v opcional, três números N separados por pontos, e um sufixo de "
        "pré-lançamento opcional (alpha, beta ou rc, com um número N opcional)."
    ),
    formal="( v | ε ) N '.' N '.' N ( - ( alpha | beta | rc ) ( '.' N | ε ) | ε )",
    padrao=PADRAO_VERSAO,
    grupos={1: "maior", 2: "menor", 3: "correção", 5: "rótulo de pré-lançamento", 7: "número do pré-lançamento"},
)

_PESO_ROTULO = {"alpha": 0, "beta": 1, "rc": 2}


@dataclass(frozen=True, slots=True)
class Versao:
    maior: int
    menor: int
    correcao: int
    pre_rotulo: str | None
    pre_numero: int | None
    prefixo_v: bool

    def chave_ordenacao(self) -> tuple[int, int, int, int, int, int]:
        estavel = self.pre_rotulo is None
        peso_rotulo = _PESO_ROTULO[self.pre_rotulo] if not estavel else 0
        numero = self.pre_numero if self.pre_numero is not None else 0
        return (self.maior, self.menor, self.correcao, int(estavel), peso_rotulo, numero)

    def __lt__(self, outra: Versao) -> bool:
        return self.chave_ordenacao() < outra.chave_ordenacao()

    def __le__(self, outra: Versao) -> bool:
        return self.chave_ordenacao() <= outra.chave_ordenacao()

    def __gt__(self, outra: Versao) -> bool:
        return self.chave_ordenacao() > outra.chave_ordenacao()

    def __ge__(self, outra: Versao) -> bool:
        return self.chave_ordenacao() >= outra.chave_ordenacao()


def validar_versao(tag: str) -> Versao | None:
    correspondencia = re.fullmatch(PADRAO_VERSAO, tag)
    if correspondencia is None:
        return None
    maior, menor, correcao, _, rotulo, _, numero = correspondencia.groups()
    return Versao(
        maior=int(maior),
        menor=int(menor),
        correcao=int(correcao),
        pre_rotulo=rotulo,
        pre_numero=int(numero) if numero is not None else None,
        prefixo_v=tag.startswith("v"),
    )
