from __future__ import annotations

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
