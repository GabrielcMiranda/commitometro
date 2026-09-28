from datetime import datetime, timezone

from commitometro.analise import analisar_commit
from commitometro.modelos import Commit
from commitometro.versionamento import sugerir_versao, ultima_versao_estavel


def _analises(*mensagens: str):
    return [
        analisar_commit(
            Commit(
                hash="0" * 40,
                autor_nome="Ana Souza",
                autor_email="ana@example.com",
                data=datetime(2026, 8, 1, tzinfo=timezone.utc),
                mensagem=mensagem,
                merge=False,
            )
        )
        for mensagem in mensagens
    ]


def test_ultima_tag_estavel_ignora_pre_lancamento_e_invalidas() -> None:
    tag, versao = ultima_versao_estavel(["v1.9.0", "v1.10.0", "v2.0.0-rc.1", "versao-final"])
    assert tag == "v1.10.0"
    assert (versao.maior, versao.menor) == (1, 10)


def test_sem_tag_estavel_nao_ha_base() -> None:
    assert ultima_versao_estavel(["v1.0.0-beta.1", "release"]) is None


def test_quebra_sobe_versao_maior() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("feat: a", "fix(api)!: muda rota"))
    assert sugestao.versao_anterior == "v1.4.2"
    assert sugestao.versao_sugerida == "v2.0.0"
    assert sugestao.tipo_incremento == "maior"
    assert "quebra de compatibilidade" in sugestao.motivo


def test_breaking_change_no_rodape_sobe_versao_maior() -> None:
    analises = _analises("refactor: troca formato\n\nBREAKING CHANGE: campo renomeado")
    assert sugerir_versao(["v1.4.2"], analises).versao_sugerida == "v2.0.0"


def test_feat_sobe_versao_menor() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("feat: a", "feat: b", "fix: c"))
    assert sugestao.versao_sugerida == "v1.5.0"
    assert sugestao.motivo == "2 commits feat → versão menor"


def test_fix_e_perf_sobem_versao_de_correcao() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("fix: a", "perf: b", "docs: c"))
    assert sugestao.versao_sugerida == "v1.4.3"
    assert sugestao.tipo_incremento == "correcao"


def test_so_docs_nao_gera_versao_nova() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("docs: a", "chore: b"))
    assert sugestao.versao_sugerida == "v1.4.2"
    assert sugestao.tipo_incremento == "nenhum"


def test_commits_invalidos_nao_entram_no_calculo() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("Feat: a", "feature!: b", "docs: c"))
    assert sugestao.tipo_incremento == "nenhum"


def test_sem_tags_parte_de_zero() -> None:
    sugestao = sugerir_versao([], _analises("feat: primeira funcionalidade"))
    assert sugestao.versao_anterior is None
    assert sugestao.versao_sugerida == "v0.1.0"


def test_so_pre_lancamentos_parte_de_zero() -> None:
    sugestao = sugerir_versao(["v1.0.0-rc.1"], _analises("fix: a"))
    assert sugestao.versao_sugerida == "v0.0.1"


def test_mantem_ausencia_do_prefixo_v() -> None:
    assert sugerir_versao(["1.4.2"], _analises("feat: a")).versao_sugerida == "1.5.0"


def test_pre_lancamento_comeca_em_um() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("feat: a"), pre="beta")
    assert sugestao.versao_sugerida == "v1.5.0-beta.1"


def test_pre_lancamento_incrementa_numero_existente() -> None:
    tags = ["v1.4.2", "v1.5.0-beta.1", "v1.5.0-beta.2", "v1.5.0-alpha.7"]
    sugestao = sugerir_versao(tags, _analises("feat: a"), pre="beta")
    assert sugestao.versao_sugerida == "v1.5.0-beta.3"


def test_pre_lancamento_sem_incremento_nao_gera_versao() -> None:
    sugestao = sugerir_versao(["v1.4.2"], _analises("docs: a"), pre="rc")
    assert sugestao.versao_sugerida == "v1.4.2"
