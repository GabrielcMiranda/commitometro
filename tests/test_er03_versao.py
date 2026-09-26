import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.versionamento import validar_versao

_DADOS = carregar_casos("er03_versao.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_versao(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_versao(cadeia) is None


def test_extrai_versao_com_pre_lancamento() -> None:
    resultado = validar_versao("v2.1.0-beta.3")
    assert resultado is not None
    assert resultado.prefixo_v is True
    assert (resultado.maior, resultado.menor, resultado.correcao) == (2, 1, 0)
    assert resultado.pre_rotulo == "beta"
    assert resultado.pre_numero == 3


def test_versao_estavel_e_maior_que_pre_lancamento_da_mesma_base() -> None:
    estavel = validar_versao("1.0.0")
    pre = validar_versao("1.0.0-rc.1")
    assert estavel is not None
    assert pre is not None
    assert estavel > pre


def test_ordem_dos_rotulos_de_pre_lancamento() -> None:
    alpha = validar_versao("1.0.0-alpha.1")
    beta = validar_versao("1.0.0-beta.1")
    rc = validar_versao("1.0.0-rc.1")
    assert alpha is not None
    assert beta is not None
    assert rc is not None
    assert alpha < beta < rc


def test_operadores_le_e_ge_entre_versoes_iguais() -> None:
    primeira = validar_versao("1.2.3")
    segunda = validar_versao("1.2.3")
    assert primeira is not None
    assert segunda is not None
    assert primeira <= segunda
    assert primeira >= segunda
