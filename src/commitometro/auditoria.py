from __future__ import annotations

from pathlib import Path

from commitometro.analise import analisar_commit
from commitometro.conformidade import (
    calcular_conformidade,
    classificar_branches,
    classificar_tags,
)
from commitometro.erros import EntradaInvalidaError
from commitometro.leitores.arquivo import ler_historico, ler_linhas
from commitometro.leitores.repositorio import (
    commits_desde,
    ler_branches,
    ler_commits,
    ler_tags,
)
from commitometro.modelos import AnaliseCommit, Commit, RelatorioAuditoria
from commitometro.versionamento import sugerir_versao, ultima_versao_estavel


def _ler_repositorio(
    caminho: str | Path, incluir_merges: bool
) -> tuple[list[Commit], list[str], list[str], set[str] | None]:
    commits = ler_commits(caminho, incluir_merges)
    tags = ler_tags(caminho)
    branches = ler_branches(caminho)
    base = ultima_versao_estavel(tags)
    hashes_desde_base = set(commits_desde(caminho, base[0])) if base else None
    return commits, tags, branches, hashes_desde_base


def _ler_arquivos(
    historico: str | Path, arquivo_tags: str | Path | None, arquivo_branches: str | Path | None
) -> tuple[list[Commit], list[str], list[str], set[str] | None]:
    commits = ler_historico(historico)
    tags = ler_linhas(arquivo_tags) if arquivo_tags is not None else []
    branches = ler_linhas(arquivo_branches) if arquivo_branches is not None else []
    return commits, tags, branches, None


def _analises_para_versao(
    analises: list[AnaliseCommit], hashes_desde_base: set[str] | None
) -> list[AnaliseCommit]:
    if hashes_desde_base is None:
        return analises
    return [analise for analise in analises if analise.commit.hash in hashes_desde_base]


def auditar(
    caminho_repositorio: str | Path | None = None,
    *,
    historico: str | Path | None = None,
    arquivo_tags: str | Path | None = None,
    arquivo_branches: str | Path | None = None,
    incluir_merges: bool = False,
    pre: str | None = None,
) -> RelatorioAuditoria:
    if (caminho_repositorio is None) == (historico is None):
        raise EntradaInvalidaError(
            "Informe o caminho de um repositório ou um arquivo de histórico exportado, "
            "mas não os dois."
        )
    if caminho_repositorio is not None:
        commits, tags, branches, hashes = _ler_repositorio(caminho_repositorio, incluir_merges)
    else:
        commits, tags, branches, hashes = _ler_arquivos(historico, arquivo_tags, arquivo_branches)

    analises = [analisar_commit(commit) for commit in commits]
    branches_validas, branches_invalidas = classificar_branches(branches)
    tags_validas, tags_invalidas = classificar_tags(tags)
    return RelatorioAuditoria(
        por_autor=tuple(calcular_conformidade(analises)),
        branches_validas=branches_validas,
        branches_invalidas=branches_invalidas,
        tags_validas=tags_validas,
        tags_invalidas=tags_invalidas,
        sugestao_versao=sugerir_versao(tags, _analises_para_versao(analises, hashes), pre),
    )
