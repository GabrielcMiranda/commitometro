from datetime import datetime, timezone

from commitometro.analise import analisar_commit
from commitometro.conformidade import (
    calcular_conformidade,
    classificar_branches,
    classificar_tags,
)
from commitometro.modelos import Commit


def _analise(mensagem: str, nome: str, email: str):
    commit = Commit(
        hash="0" * 40,
        autor_nome=nome,
        autor_email=email,
        data=datetime(2026, 8, 1, tzinfo=timezone.utc),
        mensagem=mensagem,
        merge=False,
    )
    return analisar_commit(commit)


def test_agrega_metricas_por_autor() -> None:
    analises = [
        _analise("feat(auth): login\n\nCloses #1", "Ana Souza", "ana@example.com"),
        _analise("fix(auth)!: troca token", "Ana Souza", "ana@example.com"),
        _analise("Adiciona botão", "Ana Souza", "ana@example.com"),
        _analise("docs: readme", "Rui Costa", "rui@example.com"),
    ]
    ana, rui = calcular_conformidade(analises)
    assert (ana.nome, ana.total_commits, ana.commits_validos) == ("Ana Souza", 3, 2)
    assert ana.percentual_conformidade == 66.7
    assert ana.distribuicao_por_tipo == {"feat": 1, "fix": 1}
    assert ana.commits_com_issue == 1
    assert ana.quebras_declaradas == 1
    assert len(ana.invalidos) == 1
    assert ana.invalidos[0].diagnostico is not None
    assert rui.percentual_conformidade == 100.0


def test_agrupa_email_sem_diferenciar_maiusculas() -> None:
    analises = [
        _analise("feat: a", "Ana Souza", "Ana@Example.com"),
        _analise("feat: b", "Ana S.", "ana@example.com"),
        _analise("feat: c", "Ana Souza", "ana@example.com"),
    ]
    (autora,) = calcular_conformidade(analises)
    assert autora.total_commits == 3
    assert autora.nome == "Ana Souza"


def test_autor_sem_nenhum_commit_valido() -> None:
    (autor,) = calcular_conformidade([_analise("Corrige: bug", "Rui Costa", "rui@example.com")])
    assert autor.commits_validos == 0
    assert autor.percentual_conformidade == 0.0
    assert autor.distribuicao_por_tipo == {}


def test_credita_coautoria_a_quem_nao_e_o_autor() -> None:
    analises = [
        _analise(
            "feat: cupom\n\nCo-authored-by: Rui Costa <RUI@example.com>\n"
            "Co-authored-by: Ana Souza <ana@example.com>",
            "Ana Souza",
            "ana@example.com",
        ),
        _analise("docs: readme", "Rui Costa", "rui@example.com"),
    ]
    por_email = {autor.email: autor for autor in calcular_conformidade(analises)}
    assert por_email["rui@example.com"].coautorias_recebidas == 1
    assert por_email["ana@example.com"].coautorias_recebidas == 0


def test_ordena_por_quantidade_de_commits() -> None:
    analises = [
        _analise("docs: a", "Rui Costa", "rui@example.com"),
        _analise("feat: b", "Ana Souza", "ana@example.com"),
        _analise("feat: c", "Ana Souza", "ana@example.com"),
    ]
    assert [autor.nome for autor in calcular_conformidade(analises)] == ["Ana Souza", "Rui Costa"]


def test_classifica_branches() -> None:
    validas, invalidas = classificar_branches(["main", "feature/login", "master", "feat/x"])
    assert validas == ("main", "feature/login")
    assert invalidas == ("master", "feat/x")


def test_classifica_tags() -> None:
    validas, invalidas = classificar_tags(["v1.0.0", "2.0.0-rc.1", "versao-final", "1.0"])
    assert validas == ("v1.0.0", "2.0.0-rc.1")
    assert invalidas == ("versao-final", "1.0")
