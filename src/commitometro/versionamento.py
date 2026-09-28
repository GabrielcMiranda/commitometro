from __future__ import annotations

from collections.abc import Iterable

from commitometro.padroes.versionamento import Versao, validar_versao


def ultima_versao_estavel(tags: Iterable[str]) -> tuple[str, Versao] | None:
    estaveis = []
    for tag in tags:
        versao = validar_versao(tag)
        if versao is not None and versao.pre_rotulo is None:
            estaveis.append((tag, versao))
    if not estaveis:
        return None
    return max(estaveis, key=lambda par: par[1].chave_ordenacao())
