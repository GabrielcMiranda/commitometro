from __future__ import annotations

from pathlib import Path

import git
from pydriller import Repository

from commitometro.erros import EntradaInvalidaError
from commitometro.modelos import Commit


def _validar_caminho(caminho: Path) -> None:
    if not caminho.exists():
        raise EntradaInvalidaError(f"O caminho '{caminho}' não existe.")


def ler_commits(caminho: str | Path, incluir_merges: bool = False) -> list[Commit]:
    caminho = Path(caminho)
    _validar_caminho(caminho)
    try:
        commits = [
            Commit(
                hash=commit.hash,
                autor_nome=commit.author.name,
                autor_email=commit.author.email,
                data=commit.author_date,
                mensagem=commit.msg,
                merge=commit.merge,
            )
            for commit in Repository(str(caminho)).traverse_commits()
            if incluir_merges or not commit.merge
        ]
    except git.exc.InvalidGitRepositoryError as erro:
        raise EntradaInvalidaError(f"A pasta '{caminho}' não é um repositório Git.") from erro
    except git.exc.GitCommandNotFound as erro:
        raise EntradaInvalidaError("O git não foi encontrado no PATH.") from erro
    if not commits:
        raise EntradaInvalidaError(f"O repositório em '{caminho}' não tem nenhum commit.")
    return commits


def _abrir_repositorio(caminho: Path) -> git.Repo:
    _validar_caminho(caminho)
    try:
        return git.Repo(caminho)
    except git.exc.InvalidGitRepositoryError as erro:
        raise EntradaInvalidaError(f"A pasta '{caminho}' não é um repositório Git.") from erro
    except git.exc.GitCommandNotFound as erro:
        raise EntradaInvalidaError("O git não foi encontrado no PATH.") from erro


def ler_tags(caminho: str | Path) -> list[str]:
    repositorio = _abrir_repositorio(Path(caminho))
    return [str(tag) for tag in repositorio.tags]


def ler_branches(caminho: str | Path) -> list[str]:
    repositorio = _abrir_repositorio(Path(caminho))
    locais = [str(ramo) for ramo in repositorio.branches]
    remotas = []
    if repositorio.remotes:
        for referencia in repositorio.remote().refs:
            if referencia.name.endswith("/HEAD"):
                continue
            remotas.append(referencia.name.split("/", 1)[-1])
    return list(dict.fromkeys(locais + remotas))


def commits_desde(caminho: str | Path, tag: str) -> list[str]:
    repositorio = _abrir_repositorio(Path(caminho))
    return [commit.hexsha for commit in repositorio.iter_commits(f"{tag}..HEAD")]
