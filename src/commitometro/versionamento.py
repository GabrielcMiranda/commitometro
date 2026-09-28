from __future__ import annotations

from collections.abc import Iterable

from commitometro.modelos import AnaliseCommit, SugestaoVersao
from commitometro.padroes.versionamento import Versao, validar_versao

_TIPOS_DE_CORRECAO = {"fix", "perf"}

_NOME_DO_INCREMENTO = {"maior": "maior", "menor": "menor", "correcao": "de correção"}


def ultima_versao_estavel(tags: Iterable[str]) -> tuple[str, Versao] | None:
    estaveis = []
    for tag in tags:
        versao = validar_versao(tag)
        if versao is not None and versao.pre_rotulo is None:
            estaveis.append((tag, versao))
    if not estaveis:
        return None
    return max(estaveis, key=lambda par: par[1].chave_ordenacao())


def _plural(quantidade: int, singular: str, plural: str) -> str:
    return f"{quantidade} {singular if quantidade == 1 else plural}"


def _proximo_numero_de_pre(tags: list[str], numeros: tuple[int, int, int], rotulo: str) -> int:
    existentes = [
        versao.pre_numero or 0
        for versao in (validar_versao(tag) for tag in tags)
        if versao is not None
        and (versao.maior, versao.menor, versao.correcao) == numeros
        and versao.pre_rotulo == rotulo
    ]
    return max(existentes) + 1 if existentes else 1


def sugerir_versao(
    tags: Iterable[str],
    analises: Iterable[AnaliseCommit],
    pre: str | None = None,
) -> SugestaoVersao:
    tags = list(tags)
    base = ultima_versao_estavel(tags)
    tag_anterior, versao = base if base else (None, Versao(0, 0, 0, None, None, True))
    prefixo = "v" if versao.prefixo_v else ""
    validas = [analise for analise in analises if analise.valido]
    quebras = sum(1 for analise in validas if analise.quebra)
    features = sum(1 for analise in validas if analise.tipo == "feat")
    correcoes = sum(1 for analise in validas if analise.tipo in _TIPOS_DE_CORRECAO)

    if quebras:
        numeros = (versao.maior + 1, 0, 0)
        tipo = "maior"
        motivo = _plural(quebras, "commit com quebra de compatibilidade", "commits com quebra de compatibilidade")
    elif features:
        numeros = (versao.maior, versao.menor + 1, 0)
        tipo = "menor"
        motivo = _plural(features, "commit feat", "commits feat")
    elif correcoes:
        numeros = (versao.maior, versao.menor, versao.correcao + 1)
        tipo = "correcao"
        motivo = _plural(correcoes, "commit fix/perf", "commits fix/perf")
    else:
        numeros = (versao.maior, versao.menor, versao.correcao)
        tipo = "nenhum"
        motivo = "nenhum commit válido com quebra, feat, fix ou perf"

    versao_sugerida = prefixo + ".".join(str(numero) for numero in numeros)
    if pre is not None and tipo != "nenhum":
        versao_sugerida += f"-{pre}.{_proximo_numero_de_pre(tags, numeros, pre)}"

    return SugestaoVersao(
        versao_anterior=tag_anterior,
        versao_sugerida=versao_sugerida,
        tipo_incremento=tipo,
        motivo=(
            f"{motivo} → versão {_NOME_DO_INCREMENTO[tipo]}"
            if tipo != "nenhum"
            else f"{motivo} → sem nova versão"
        ),
    )
