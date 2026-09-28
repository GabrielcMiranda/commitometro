from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from commitometro.modelos import AnaliseCommit, ConformidadeAutor


def _agrupar_por_email(analises: list[AnaliseCommit]) -> dict[str, list[AnaliseCommit]]:
    grupos: dict[str, list[AnaliseCommit]] = {}
    for analise in analises:
        grupos.setdefault(analise.commit.autor_email.lower(), []).append(analise)
    return grupos


def _conformidade_do_autor(email: str, analises: list[AnaliseCommit]) -> ConformidadeAutor:
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
        coautorias_recebidas=0,
        invalidos=tuple(analise for analise in analises if not analise.valido),
    )


def calcular_conformidade(analises: Iterable[AnaliseCommit]) -> list[ConformidadeAutor]:
    grupos = _agrupar_por_email(list(analises))
    resultado = [_conformidade_do_autor(email, lista) for email, lista in grupos.items()]
    return sorted(resultado, key=lambda autor: (-autor.total_commits, autor.nome))
