import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.commits import validar_cabecalho

_DADOS = carregar_casos("er01_cabecalho.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_cabecalho(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_cabecalho(cadeia) is None


def test_extrai_tipo_escopo_quebra_e_descricao() -> None:
    resultado = validar_cabecalho("feat(api-v2)!: remove endpoint legado")
    assert resultado is not None
    assert resultado.tipo == "feat"
    assert resultado.escopo == "api-v2"
    assert resultado.quebra is True
    assert resultado.descricao == "remove endpoint legado"


def test_extrai_sem_escopo_e_sem_quebra() -> None:
    resultado = validar_cabecalho("docs: x")
    assert resultado is not None
    assert resultado.tipo == "docs"
    assert resultado.escopo is None
    assert resultado.quebra is False
    assert resultado.descricao == "x"
