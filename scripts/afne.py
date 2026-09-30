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

    def _satisfaz(self, rotulo: str, caractere: str) -> bool:
        espaco = self.legenda.get("espaco")
        if rotulo == espaco:
            return caractere == " "
        classes = self.legenda.get("classes", {})
        if rotulo in classes:
            predicado = classes[rotulo]
            if "intervalos" in predicado:
                return any(inicio <= caractere <= fim for inicio, fim in predicado["intervalos"])
            if "conjunto" in predicado:
                return caractere in predicado["conjunto"]
            if "exceto" in predicado:
                return caractere not in predicado["exceto"]
            return False
        return caractere == rotulo

    def _fecho_epsilon(self, conjunto: set[int]) -> set[int]:
        pilha = list(conjunto)
        fechado = set(conjunto)
        while pilha:
            atual = pilha.pop()
            for rotulo, destino in self.transicoes.get(atual, []):
                if rotulo is None and destino not in fechado:
                    fechado.add(destino)
                    pilha.append(destino)
        return fechado

    def aceita(self, cadeia: str) -> bool:
        atuais = self._fecho_epsilon({self.inicial})
        for caractere in cadeia:
            proximos: set[int] = set()
            for estado in atuais:
                for rotulo, destino in self.transicoes.get(estado, []):
                    if rotulo is not None and self._satisfaz(rotulo, caractere):
                        proximos.add(destino)
            atuais = self._fecho_epsilon(proximos)
            if not atuais:
                return False
        return bool(atuais & self.finais)


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
