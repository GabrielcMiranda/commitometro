from __future__ import annotations

from commitometro.modelos import AnaliseCommit, Commit
from commitometro.padroes.commits import Rodape, validar_cabecalho, validar_rodape


def _paragrafos(mensagem: str) -> list[list[str]]:
    paragrafos: list[list[str]] = []
    atual: list[str] = []
    for linha in mensagem.splitlines():
        if linha.strip():
            atual.append(linha)
        elif atual:
            paragrafos.append(atual)
            atual = []
    if atual:
        paragrafos.append(atual)
    return paragrafos


def bloco_de_rodape(mensagem: str) -> list[Rodape]:
    paragrafos = _paragrafos(mensagem)
    if len(paragrafos) < 2:
        return []
    rodapes = [validar_rodape(linha) for linha in paragrafos[-1]]
    if any(rodape is None for rodape in rodapes):
        return []
    return rodapes


def analisar_commit(commit: Commit) -> AnaliseCommit:
    linhas = commit.mensagem.splitlines()
    primeira_linha = linhas[0] if linhas else ""
    cabecalho = validar_cabecalho(primeira_linha)
    quebra_no_rodape = any(rodape.quebra for rodape in bloco_de_rodape(commit.mensagem))
    return AnaliseCommit(
        commit=commit,
        tipo=cabecalho.tipo if cabecalho else None,
        escopo=cabecalho.escopo if cabecalho else None,
        quebra=(cabecalho is not None and cabecalho.quebra) or quebra_no_rodape,
        valido=cabecalho is not None,
        diagnostico=None,
        issues=(),
        coautores=(),
    )
