from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.etree import ElementTree


def _ler_estrutura(caminho_jff: str | Path):
    raiz = ElementTree.parse(caminho_jff).getroot()
    estados: list[int] = []
    inicial: int | None = None
    finais: set[int] = set()
    for estado in raiz.iter("state"):
        id_estado = int(estado.get("id"))
        estados.append(id_estado)
        if estado.find("initial") is not None:
            inicial = id_estado
        if estado.find("final") is not None:
            finais.add(id_estado)

    transicoes: list[tuple[int, str | None, int]] = []
    for transicao in raiz.iter("transition"):
        origem = int(transicao.findtext("from"))
        destino = int(transicao.findtext("to"))
        rotulo = transicao.findtext("read") or None
        transicoes.append((origem, rotulo, destino))

    return sorted(estados), inicial, finais, transicoes


def _descrever_predicado(predicado: dict) -> str:
    if "intervalos" in predicado:
        return " ∪ ".join(f"[{inicio}-{fim}]" for inicio, fim in predicado["intervalos"])
    if "conjunto" in predicado:
        return "{" + ", ".join(predicado["conjunto"]) + "}"
    if "exceto" in predicado:
        excecoes = ", ".join(repr(c)[1:-1] for c in predicado["exceto"])
        return f"Σ − {{{excecoes}}}"
    return "?"


def gerar_markdown(caminho_jff: str | Path, caminho_legenda: str | Path, id_er: str) -> str:
    estados, inicial, finais, transicoes = _ler_estrutura(caminho_jff)
    legenda = json.loads(Path(caminho_legenda).read_text(encoding="utf-8"))
    alfabeto = sorted({rotulo for _, rotulo, _ in transicoes if rotulo is not None})

    linhas = [f"# {id_er} — 5-upla e tabela de transição", "", "## 5-upla M = (Q, Σ, δ, q0, F)", ""]
    linhas.append(f"- Q = {{{', '.join(f'q{e}' for e in estados)}}} ({len(estados)} estados)")
    linhas.append(f"- Σ = {{{', '.join(alfabeto)}}} (símbolos de arco; classes na legenda abaixo)")
    linhas.append(f"- q0 = q{inicial}")
    linhas.append(f"- F = {{{', '.join(f'q{e}' for e in sorted(finais))}}}")
    linhas.append(f"- δ: {len(transicoes)} transições (tabela abaixo)")

    linhas += ["", "## Tabela de transição δ", ""]
    colunas = ["ε"] + alfabeto
    linhas.append("| Estado | " + " | ".join(colunas) + " |")
    linhas.append("|" + "---|" * (len(colunas) + 1))

    por_estado: dict[int, dict[str | None, list[int]]] = {}
    for origem, rotulo, destino in transicoes:
        por_estado.setdefault(origem, {}).setdefault(rotulo, []).append(destino)

    for estado in estados:
        celulas = [", ".join(f"q{d}" for d in por_estado.get(estado, {}).get(None, [])) or "—"]
        for simbolo in alfabeto:
            celulas.append(", ".join(f"q{d}" for d in por_estado.get(estado, {}).get(simbolo, [])) or "—")
        nome = f"q{estado}"
        if estado == inicial:
            nome = f"→{nome}"
        if estado in finais:
            nome = f"*{nome}"
        linhas.append(f"| {nome} | " + " | ".join(celulas) + " |")

    linhas += ["", "## Legenda dos símbolos de classe", ""]
    espaco = legenda.get("espaco")
    if espaco:
        linhas.append(f"- `{espaco}` representa o caractere real `' '` (espaço).")
    classes = legenda.get("classes", {})
    for simbolo, predicado in classes.items():
        linhas.append(f"- `{simbolo}` = {_descrever_predicado(predicado)}")
    if not espaco and not classes:
        linhas.append("- Nenhum símbolo de classe nesta ER; todo arco é um caractere literal.")

    linhas.append("")
    linhas.append(f"(`→` = estado inicial, `*` = estado final; {len(estados)} estados, {len(transicoes)} transições.)")
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    id_er = sys.argv[1] if len(sys.argv) > 1 else "exemplo_numero"
    caminho_jff = Path("docs/afne") / f"{id_er}.jff"
    caminho_legenda = Path("docs/afne") / f"{id_er}.legenda.json"
    caminho_saida = Path("docs/afne") / f"{id_er}.md"
    caminho_saida.write_text(gerar_markdown(caminho_jff, caminho_legenda, id_er), encoding="utf-8")
    print(f"Tabela gerada em {caminho_saida}")
