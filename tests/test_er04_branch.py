import pytest
from casos_util import cadeias_aceitas, cadeias_rejeitadas, carregar_casos

from commitometro.padroes.versionamento import validar_branch

_DADOS = carregar_casos("er04_branch.json")


@pytest.mark.parametrize("cadeia", cadeias_aceitas(_DADOS))
def test_aceita(cadeia: str) -> None:
    assert validar_branch(cadeia) is not None


@pytest.mark.parametrize("cadeia", cadeias_rejeitadas(_DADOS))
def test_rejeita(cadeia: str) -> None:
    assert validar_branch(cadeia) is None


def test_categoria_main_e_develop_sem_descricao() -> None:
    assert validar_branch("main").categoria == "main"
    assert validar_branch("main").descricao is None
    assert validar_branch("develop").categoria == "develop"


def test_extrai_categoria_e_descricao_de_feature() -> None:
    resultado = validar_branch("feature/42-recuperar-senha")
    assert resultado is not None
    assert resultado.categoria == "feature"
    assert resultado.descricao == "42-recuperar-senha"


def test_extrai_categoria_e_versao_de_release() -> None:
    resultado = validar_branch("release/1.4.0")
    assert resultado is not None
    assert resultado.categoria == "release"
    assert resultado.descricao == "1.4.0"
