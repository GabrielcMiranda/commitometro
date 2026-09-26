import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.commits import validar_rodape

_DADOS = carregar_casos("er02_rodape.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_rodape(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_rodape(cadeia) is None


def test_detecta_quebra_com_breaking_change() -> None:
    resultado = validar_rodape("BREAKING CHANGE: remove suporte ao Python 3.11")
    assert resultado is not None
    assert resultado.quebra is True
    assert resultado.valor == "remove suporte ao Python 3.11"


def test_nao_detecta_quebra_em_outros_tokens() -> None:
    resultado = validar_rodape("Closes #42")
    assert resultado is not None
    assert resultado.quebra is False
    assert resultado.token == "Closes"
    assert resultado.separador == " #"
