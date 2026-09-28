from __future__ import annotations

from pathlib import Path

import git
from pydriller import Repository

from commitometro.modelos import Commit


def ler_commits(caminho: str | Path, incluir_merges: bool = False) -> list[Commit]:
    caminho = Path(caminho)
    return [
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


def ler_tags(caminho: str | Path) -> list[str]:
    repositorio = git.Repo(caminho)
    return [str(tag) for tag in repositorio.tags]


def ler_branches(caminho: str | Path) -> list[str]:
    repositorio = git.Repo(caminho)
    locais = [str(ramo) for ramo in repositorio.branches]
    remotas = []
    if repositorio.remotes:
        for referencia in repositorio.remote().refs:
            if referencia.name.endswith("/HEAD"):
                continue
            remotas.append(referencia.name.split("/", 1)[-1])
    return list(dict.fromkeys(locais + remotas))


def commits_desde(caminho: str | Path, tag: str) -> list[str]:
    repositorio = git.Repo(caminho)
    return [commit.hexsha for commit in repositorio.iter_commits(f"{tag}..HEAD")]
