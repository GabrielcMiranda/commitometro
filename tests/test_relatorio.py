import json
from dataclasses import replace

from rich.console import Console

from commitometro.auditoria import auditar
from commitometro.relatorio import para_json, para_markdown, renderizar_tabela

CAMINHO_HISTORICO = "dados/exemplos/historico_exemplo.log"
CAMINHO_TAGS = "dados/exemplos/tags_exemplo.txt"
CAMINHO_BRANCHES = "dados/exemplos/branches_exemplo.txt"


def _relatorio_de_exemplo():
    return auditar(
        historico=CAMINHO_HISTORICO,
        arquivo_tags=CAMINHO_TAGS,
        arquivo_branches=CAMINHO_BRANCHES,
    )


def test_renderiza_tabela_sem_lancar_excecao() -> None:
    console = Console(record=True, width=100)
    renderizar_tabela(console, _relatorio_de_exemplo())
    texto = console.export_text()
    assert "Resumo da auditoria" in texto
    assert "Conformidade por autor" in texto
    assert "Sugestão de versão" in texto


def test_renderiza_lista_de_invalidos_quando_ha() -> None:
    console = Console(record=True, width=100)
    renderizar_tabela(console, _relatorio_de_exemplo())
    assert "Commits inválidos" in console.export_text()


def test_para_json_e_valido_e_completo() -> None:
    dados = json.loads(para_json(_relatorio_de_exemplo()))
    assert len(dados["por_autor"]) == 4
    assert "sugestao_versao" in dados
    assert dados["sugestao_versao"]["tipo_incremento"] == "maior"
    primeiro_autor = dados["por_autor"][0]
    assert "distribuicao_por_tipo" in primeiro_autor
    assert isinstance(primeiro_autor["invalidos"], list)


def test_para_markdown_tem_as_secoes_esperadas() -> None:
    texto = para_markdown(_relatorio_de_exemplo())
    assert texto.startswith("# Relatório de auditoria")
    assert "## Conformidade por autor" in texto
    assert "## Branches" in texto
    assert "## Tags" in texto
    assert "## Sugestão de versão" in texto
    assert "## Commits inválidos" in texto


def test_para_markdown_omite_secao_de_invalidos_quando_nao_ha() -> None:
    relatorio = _relatorio_de_exemplo()
    relatorio_sem_invalidos = replace(
        relatorio,
        por_autor=tuple(replace(autor, invalidos=()) for autor in relatorio.por_autor),
    )
    assert "Commits inválidos" not in para_markdown(relatorio_sem_invalidos)
