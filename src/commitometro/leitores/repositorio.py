from __future__ import annotations

from pathlib import Path

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
