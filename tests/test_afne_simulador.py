import re

import pytest

from scripts.afne import carregar

CAMINHO_JFF = "docs/afne/exemplo_numero.jff"
CAMINHO_LEGENDA = "docs/afne/exemplo_numero.legenda.json"
PADRAO_NUMERO = r"0|[1-9][0-9]*"


@pytest.fixture(scope="module")
def afne_exemplo():
    return carregar(CAMINHO_JFF, CAMINHO_LEGENDA)


@pytest.mark.parametrize("cadeia", ["0", "7", "105", "999"])
def test_aceita_numeros_validos(afne_exemplo, cadeia: str) -> None:
    assert afne_exemplo.aceita(cadeia) is True


@pytest.mark.parametrize("cadeia", ["", "01", "00", "a", "9a", "-1"])
def test_rejeita_numeros_invalidos(afne_exemplo, cadeia: str) -> None:
    assert afne_exemplo.aceita(cadeia) is False


@pytest.mark.parametrize(
    "cadeia",
    ["0", "1", "7", "10", "42", "999", "", "00", "01", "007", "a", "1a", "-5", "10.5"],
)
def test_concorda_com_a_regex_equivalente(afne_exemplo, cadeia: str) -> None:
    esperado = re.fullmatch(PADRAO_NUMERO, cadeia) is not None
    assert afne_exemplo.aceita(cadeia) == esperado
