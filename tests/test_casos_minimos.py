import pytest
from casos_util import DIRETORIO_CASOS, carregar_casos


def _arquivos_de_casos() -> list[str]:
    return sorted(caminho.name for caminho in DIRETORIO_CASOS.glob("*.json"))


@pytest.mark.parametrize("nome_arquivo", _arquivos_de_casos())
def test_quantidade_minima_de_casos(nome_arquivo: str) -> None:
    dados = carregar_casos(nome_arquivo)
    aceitas = dados["aceitas"]
    rejeitadas = dados["rejeitadas"]
    assert len(aceitas) >= 6
    assert len(rejeitadas) >= 6
    limites = [item for item in aceitas + rejeitadas if item.get("limite")]
    assert len(limites) >= 1
