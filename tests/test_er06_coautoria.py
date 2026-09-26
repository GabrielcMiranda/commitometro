import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.referencias import validar_coautoria

_DADOS = carregar_casos("er06_coautoria.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_coautoria(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_coautoria(cadeia) is None


def test_extrai_nome_e_email() -> None:
    resultado = validar_coautoria("Co-authored-by: Ana Souza <ana.souza@gmail.com>")
    assert resultado is not None
    assert resultado.nome == "Ana Souza"
    assert resultado.email == "ana.souza@gmail.com"


def test_normaliza_email_para_minusculas() -> None:
    resultado = validar_coautoria("Co-authored-By: Rui Costa <RUI.COSTA@EMPRESA.COM.BR>")
    assert resultado is not None
    assert resultado.email == "rui.costa@empresa.com.br"


def test_aceita_coautoria_de_ia_com_versao_do_modelo() -> None:
    resultado = validar_coautoria("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    assert resultado is not None
    assert resultado.nome == "Claude Opus 5.5"
    assert resultado.email == "noreply@anthropic.com"
