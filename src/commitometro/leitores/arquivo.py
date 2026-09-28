from __future__ import annotations

from datetime import datetime
from pathlib import Path

from commitometro.erros import EntradaInvalidaError
from commitometro.modelos import Commit

_SEPARADOR_CAMPO = "\x1f"
_SEPARADOR_REGISTRO = "\x1e"


def ler_historico(caminho: str | Path) -> list[Commit]:
    caminho = Path(caminho)
    if not caminho.exists():
        raise EntradaInvalidaError(f"O arquivo '{caminho}' não existe.")
    conteudo = caminho.read_text(encoding="utf-8")
    if not conteudo.strip():
        raise EntradaInvalidaError(f"O arquivo '{caminho}' está vazio.")
    registros = [r for r in conteudo.split(_SEPARADOR_REGISTRO) if r.strip("\n")]
    commits = []
    for indice, registro in enumerate(registros, start=1):
        campos = registro.lstrip("\n").split(_SEPARADOR_CAMPO)
        if len(campos) != 5:
            raise EntradaInvalidaError(
                f"O registro {indice} de '{caminho}' tem {len(campos)} campos; eram esperados 5."
            )
        hash_commit, autor_nome, autor_email, data_iso, mensagem = campos
        commits.append(
            Commit(
                hash=hash_commit,
                autor_nome=autor_nome,
                autor_email=autor_email,
                data=datetime.fromisoformat(data_iso),
                mensagem=mensagem.rstrip("\n"),
                merge=False,
            )
        )
    return commits


def ler_linhas(caminho: str | Path) -> list[str]:
    caminho = Path(caminho)
    if not caminho.exists():
        raise EntradaInvalidaError(f"O arquivo '{caminho}' não existe.")
    linhas = (linha.strip() for linha in caminho.read_text(encoding="utf-8").splitlines())
    return [linha for linha in linhas if linha]
