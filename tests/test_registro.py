from commitometro.padroes import REGISTRO


def test_registro_tem_as_seis_expressoes_regulares() -> None:
    assert set(REGISTRO) == {"ER-01", "ER-02", "ER-03", "ER-04", "ER-05", "ER-06"}
    for expressao in REGISTRO.values():
        assert expressao.formal
        assert expressao.padrao
        assert expressao.alfabeto
        assert expressao.linguagem
        assert expressao.compilada.pattern == expressao.padrao
