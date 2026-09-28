from datetime import datetime, timezone

import pytest

from commitometro.analise import analisar_commit, bloco_de_rodape, diagnosticar_cabecalho
from commitometro.modelos import Commit


def _commit(mensagem: str, email: str = "ana@example.com") -> Commit:
    return Commit(
        hash="0" * 40,
        autor_nome="Ana Souza",
        autor_email=email,
        data=datetime(2026, 8, 1, tzinfo=timezone.utc),
        mensagem=mensagem,
        merge=False,
    )


def test_commit_valido_extrai_tipo_e_escopo() -> None:
    analise = analisar_commit(_commit("fix(carrinho): corrige frete"))
    assert analise.valido is True
    assert analise.tipo == "fix"
    assert analise.escopo == "carrinho"
    assert analise.quebra is False
    assert analise.diagnostico is None


def test_commit_invalido_tem_diagnostico() -> None:
    analise = analisar_commit(_commit("Adiciona botão de compra"))
    assert analise.valido is False
    assert analise.tipo is None
    assert analise.diagnostico == "falta o separador ': ' entre o tipo e a descrição."


def test_mensagem_vazia_e_invalida() -> None:
    analise = analisar_commit(_commit(""))
    assert analise.valido is False
    assert analise.diagnostico == "o cabeçalho está vazio."


def test_quebra_pelo_exclamacao_do_cabecalho() -> None:
    assert analisar_commit(_commit("feat(api)!: remove rota antiga")).quebra is True


def test_quebra_pelo_rodape_breaking_change() -> None:
    mensagem = "feat(api): troca formato\n\nExplica a mudança.\n\nBREAKING CHANGE: campo renomeado\nCloses #3"
    analise = analisar_commit(_commit(mensagem))
    assert analise.quebra is True
    assert [rodape.token for rodape in bloco_de_rodape(mensagem)] == ["BREAKING CHANGE", "Closes"]


def test_ultimo_paragrafo_com_linha_comum_nao_e_rodape() -> None:
    mensagem = "feat(api): troca formato\n\nBREAKING CHANGE: campo renomeado\ne mais um texto solto"
    assert bloco_de_rodape(mensagem) == []
    assert analisar_commit(_commit(mensagem)).quebra is False


def test_mensagem_de_um_paragrafo_nao_tem_rodape() -> None:
    assert bloco_de_rodape("docs: Closes #3") == []


def test_extrai_issues_de_varias_linhas_sem_repetir() -> None:
    mensagem = "feat(carrinho): cupom\n\nResolves #7, #8\nRefs: #8, org/repo#2"
    assert analisar_commit(_commit(mensagem)).issues == ("#7", "#8", "org/repo#2")


def test_extrai_coautores_humanos_e_de_ia() -> None:
    mensagem = (
        "feat(carrinho): cupom\n\n"
        "Co-authored-by: Bia Nogueira <BIA@example.com>\n"
        "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    )
    assert analisar_commit(_commit(mensagem)).coautores == (
        "bia@example.com",
        "noreply@anthropic.com",
    )


@pytest.mark.parametrize(
    ("linha", "trecho"),
    [
        ("Feat: adiciona login", "deve ser minúsculo"),
        ("feat:adiciona login", "falta um espaço depois de ':'"),
        ("feat(): escopo vazio", "escopo entre parênteses está vazio"),
        ("feat(Login): escopo", "o escopo 'Login'"),
        ("feature: tipo inexistente", "não é aceito"),
        ("fix(auth) : espaço antes", "espaço antes de ':'"),
        ("feat:  descrição com espaço", "começa com espaço"),
        ("feat!(api): ordem invertida", "depois do escopo"),
        ("feat(api: sem fechar", "fechado com ')'"),
    ],
)
def test_diagnostico_explica_o_motivo(linha: str, trecho: str) -> None:
    assert trecho in diagnosticar_cabecalho(linha)
