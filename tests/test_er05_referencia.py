import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.referencias import validar_referencia

_DADOS = carregar_casos("er05_referencia.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_referencia(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_referencia(cadeia) is None


def test_extrai_lista_de_issues() -> None:
    resultado = validar_referencia("Resolves #7, #8, #9")
    assert resultado is not None
    assert resultado.issues == ("#7", "#8", "#9")
    assert resultado.fecha is True


def test_extrai_issue_de_outro_repositorio() -> None:
    resultado = validar_referencia("Fix #3, org/repo.js#4")
    assert resultado is not None
    assert resultado.issues == ("#3", "org/repo.js#4")


def test_refs_nao_fecha_a_issue() -> None:
    resultado = validar_referencia("Refs: #123")
    assert resultado is not None
    assert resultado.fecha is False
    assert resultado.palavra_chave == "Refs"
