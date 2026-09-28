from __future__ import annotations

from commitometro.modelos import AnaliseCommit, Commit
from commitometro.padroes.commits import validar_cabecalho


def analisar_commit(commit: Commit) -> AnaliseCommit:
    linhas = commit.mensagem.splitlines()
    primeira_linha = linhas[0] if linhas else ""
    cabecalho = validar_cabecalho(primeira_linha)
    return AnaliseCommit(
        commit=commit,
        tipo=cabecalho.tipo if cabecalho else None,
        escopo=cabecalho.escopo if cabecalho else None,
        quebra=cabecalho.quebra if cabecalho else False,
        valido=cabecalho is not None,
        diagnostico=None,
        issues=(),
        coautores=(),
    )
