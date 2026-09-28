from __future__ import annotations

from datetime import datetime
from pathlib import Path

from commitometro.modelos import Commit

_SEPARADOR_CAMPO = "\x1f"
_SEPARADOR_REGISTRO = "\x1e"


def ler_historico(caminho: str | Path) -> list[Commit]:
    caminho = Path(caminho)
    conteudo = caminho.read_text(encoding="utf-8")
    registros = [r for r in conteudo.split(_SEPARADOR_REGISTRO) if r.strip("\n")]
    commits = []
    for registro in registros:
        campos = registro.lstrip("\n").split(_SEPARADOR_CAMPO)
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
    linhas = (linha.strip() for linha in caminho.read_text(encoding="utf-8").splitlines())
    return [linha for linha in linhas if linha]
