from __future__ import annotations

import json
from pathlib import Path

DIRETORIO_CASOS = Path(__file__).parent / "casos"


def carregar_casos(nome_arquivo: str) -> dict:
    caminho = DIRETORIO_CASOS / nome_arquivo
    return json.loads(caminho.read_text(encoding="utf-8"))


def cadeias_aceitas(dados: dict) -> list[str]:
    return [item["cadeia"] for item in dados["aceitas"]]


def cadeias_rejeitadas(dados: dict) -> list[str]:
    return [item["cadeia"] for item in dados["rejeitadas"]]
