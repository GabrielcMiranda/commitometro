from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree


class AFNe:
    def __init__(
        self,
        inicial: int,
        finais: set[int],
        transicoes: dict[int, list[tuple[str | None, int]]],
        legenda: dict,
    ) -> None:
        self.inicial = inicial
        self.finais = finais
        self.transicoes = transicoes
        self.legenda = legenda


def carregar(caminho_jff: str | Path, caminho_legenda: str | Path) -> AFNe:
    raiz = ElementTree.parse(caminho_jff).getroot()
    inicial: int | None = None
    finais: set[int] = set()
    for estado in raiz.iter("state"):
        id_estado = int(estado.get("id"))
        if estado.find("initial") is not None:
            inicial = id_estado
        if estado.find("final") is not None:
            finais.add(id_estado)

    transicoes: dict[int, list[tuple[str | None, int]]] = {}
    for transicao in raiz.iter("transition"):
        origem = int(transicao.findtext("from"))
        destino = int(transicao.findtext("to"))
        rotulo = transicao.findtext("read") or None
        transicoes.setdefault(origem, []).append((rotulo, destino))

    legenda = json.loads(Path(caminho_legenda).read_text(encoding="utf-8"))
    return AFNe(inicial, finais, transicoes, legenda)
