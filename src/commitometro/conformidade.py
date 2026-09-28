from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from commitometro.modelos import AnaliseCommit, ConformidadeAutor
from commitometro.padroes.versionamento import validar_branch, validar_versao


def _agrupar_por_email(analises: list[AnaliseCommit]) -> dict[str, list[AnaliseCommit]]:
    grupos: dict[str, list[AnaliseCommit]] = {}
    for analise in analises:
        grupos.setdefault(analise.commit.autor_email.lower(), []).append(analise)
    return grupos


def _contar_coautorias(analises: list[AnaliseCommit]) -> Counter[str]:
    contagem: Counter[str] = Counter()
    for analise in analises:
        autor = analise.commit.autor_email.lower()
        for email in set(analise.coautores):
            if email != autor:
                contagem[email] += 1
    return contagem


def _conformidade_do_autor(
    email: str, analises: list[AnaliseCommit], coautorias_recebidas: int
) -> ConformidadeAutor:
    validos = [analise for analise in analises if analise.valido]
    nome = Counter(analise.commit.autor_nome for analise in analises).most_common(1)[0][0]
    return ConformidadeAutor(
        nome=nome,
        email=email,
        total_commits=len(analises),
        commits_validos=len(validos),
        percentual_conformidade=round(100 * len(validos) / len(analises), 1),
        distribuicao_por_tipo=dict(Counter(analise.tipo for analise in validos)),
        commits_com_issue=sum(1 for analise in analises if analise.issues),
        quebras_declaradas=sum(1 for analise in analises if analise.quebra),
        coautorias_recebidas=coautorias_recebidas,
        invalidos=tuple(analise for analise in analises if not analise.valido),
    )


def calcular_conformidade(analises: Iterable[AnaliseCommit]) -> list[ConformidadeAutor]:
    lista_analises = list(analises)
    grupos = _agrupar_por_email(lista_analises)
    coautorias = _contar_coautorias(lista_analises)
    resultado = [
        _conformidade_do_autor(email, lista, coautorias[email]) for email, lista in grupos.items()
    ]
    return sorted(resultado, key=lambda autor: (-autor.total_commits, autor.nome))


def classificar_branches(nomes: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    lista = list(nomes)
    validas = tuple(nome for nome in lista if validar_branch(nome) is not None)
    invalidas = tuple(nome for nome in lista if validar_branch(nome) is None)
    return validas, invalidas


def classificar_tags(tags: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    lista = list(tags)
    validas = tuple(tag for tag in lista if validar_versao(tag) is not None)
    invalidas = tuple(tag for tag in lista if validar_versao(tag) is None)
    return validas, invalidas
