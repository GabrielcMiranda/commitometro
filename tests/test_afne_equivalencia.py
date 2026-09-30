import json
import random
from pathlib import Path

import pytest

from commitometro.padroes import REGISTRO
from scripts.afne import carregar

IDS = ["ER-01", "ER-02", "ER-03", "ER-04", "ER-05", "ER-06"]

ARQUIVOS_CASOS = {
    "ER-01": "tests/casos/er01_cabecalho.json",
    "ER-02": "tests/casos/er02_rodape.json",
    "ER-03": "tests/casos/er03_versao.json",
    "ER-04": "tests/casos/er04_branch.json",
    "ER-05": "tests/casos/er05_referencia.json",
    "ER-06": "tests/casos/er06_coautoria.json",
}


def _carregar_afne(id_er: str):
    return carregar(f"docs/afne/{id_er}.jff", f"docs/afne/{id_er}.legenda.json")


def _casos_oficiais(id_er: str) -> list[tuple[str, bool]]:
    dados = json.loads(Path(ARQUIVOS_CASOS[id_er]).read_text(encoding="utf-8"))
    casos = [(caso["cadeia"], True) for caso in dados["aceitas"]]
    casos += [(caso["cadeia"], False) for caso in dados["rejeitadas"]]
    return casos


@pytest.mark.parametrize("id_er", IDS)
def test_afne_er_e_casos_oficiais_concordam(id_er: str) -> None:
    afne = _carregar_afne(id_er)
    padrao = REGISTRO[id_er].compilada
    for cadeia, esperado in _casos_oficiais(id_er):
        assert afne.aceita(cadeia) is esperado, f"{id_er}: AFNε diverge do caso oficial em {cadeia!r}"
        obtido_er = padrao.fullmatch(cadeia) is not None
        assert obtido_er is esperado, f"{id_er}: ER diverge do caso oficial em {cadeia!r}"


ALFABETOS = {
    "ER-01": "abcdefghijklmnopqrstuvwxyz0123456789()!: -",
    "ER-02": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -:#",
    "ER-03": "v0123456789.-abcehlprt",
    "ER-04": "abcdefghilmnoprstuvx0123456789/-.",
    "ER-05": "CcFfRrlosedxidvfab0123456789-./#: ,",
    "ER-06": "Co-Authredby:AnSuz0123456789.@<>_+ ",
}


@pytest.mark.parametrize("id_er", IDS)
def test_afne_e_er_concordam_em_cadeias_aleatorias(id_er: str) -> None:
    afne = _carregar_afne(id_er)
    padrao = REGISTRO[id_er].compilada
    alfabeto = ALFABETOS[id_er]
    gerador = random.Random(42)
    for _ in range(2000):
        tamanho = gerador.randint(0, 22)
        cadeia = "".join(gerador.choice(alfabeto) for _ in range(tamanho))
        esperado = padrao.fullmatch(cadeia) is not None
        assert afne.aceita(cadeia) == esperado, f"{id_er}: divergiu em cadeia aleatória {cadeia!r}"
