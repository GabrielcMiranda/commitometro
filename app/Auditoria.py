from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from commitometro.auditoria import auditar
from commitometro.erros import EntradaInvalidaError
from commitometro.relatorio import para_json, para_markdown

st.set_page_config(page_title="Commitômetro — Auditoria", page_icon="✅")
st.title("Commitômetro")
st.caption("Auditor de Convenções de Commits e Versionamento em Repositórios Git")

modo = st.radio("Fonte dos dados", ["Repositório local", "Arquivos exportados"])

caminho_repositorio = None
arquivo_historico = None
arquivo_tags = None
arquivo_branches = None

if modo == "Repositório local":
    caminho_repositorio = st.text_input("Caminho do repositório Git")
else:
    arquivo_historico = st.file_uploader("Histórico exportado (historico.log)", type=["log", "txt"])
    arquivo_tags = st.file_uploader("Tags exportadas (opcional)", type=["txt"])
    arquivo_branches = st.file_uploader("Branches exportadas (opcional)", type=["txt"])


def _salvar_temporario(arquivo_enviado, sufixo: str) -> Path:
    temporario = tempfile.NamedTemporaryFile(suffix=sufixo, delete=False)
    temporario.write(arquivo_enviado.getvalue())
    temporario.close()
    return Path(temporario.name)


if st.button("Auditar"):
    try:
        caminho_historico = (
            _salvar_temporario(arquivo_historico, ".log") if arquivo_historico else None
        )
        caminho_tags = _salvar_temporario(arquivo_tags, ".txt") if arquivo_tags else None
        caminho_branches = _salvar_temporario(arquivo_branches, ".txt") if arquivo_branches else None

        relatorio = auditar(
            caminho_repositorio,
            historico=caminho_historico,
            arquivo_tags=caminho_tags,
            arquivo_branches=caminho_branches,
        )
    except EntradaInvalidaError as erro:
        st.error(str(erro))
    else:
        total_commits = sum(autor.total_commits for autor in relatorio.por_autor)
        total_validos = sum(autor.commits_validos for autor in relatorio.por_autor)
        percentual_geral = round(100 * total_validos / total_commits, 1) if total_commits else 0.0
        sugestao = relatorio.sugestao_versao

        coluna_1, coluna_2, coluna_3 = st.columns(3)
        coluna_1.metric("Commits analisados", total_commits)
        coluna_2.metric("Conformidade geral", f"{percentual_geral}%")
        coluna_3.metric(
            "Versão sugerida",
            sugestao.versao_sugerida,
            delta=sugestao.versao_anterior or "(nenhuma tag anterior)",
            delta_color="off",
        )

        tabela_autores = pd.DataFrame(
            [
                {
                    "Autor": autor.nome,
                    "Commits": autor.total_commits,
                    "Válidos": autor.commits_validos,
                    "% conformidade": autor.percentual_conformidade,
                    "Coautorias recebidas": autor.coautorias_recebidas,
                }
                for autor in relatorio.por_autor
            ]
        )
        st.subheader("Conformidade por autor")
        st.dataframe(tabela_autores, hide_index=True)
        st.bar_chart(tabela_autores.set_index("Autor")["% conformidade"])

        invalidos = [
            (autor.nome, analise) for autor in relatorio.por_autor for analise in autor.invalidos
        ]
        if invalidos:
            with st.expander(f"{len(invalidos)} commit(s) inválido(s)"):
                for nome, analise in invalidos:
                    primeira_linha = (
                        analise.commit.mensagem.splitlines()[0] if analise.commit.mensagem else ""
                    )
                    st.markdown(f"**{analise.commit.hash[:7]}** ({nome}) — `{primeira_linha}`")
                    st.caption(analise.diagnostico or "")

        coluna_json, coluna_markdown = st.columns(2)
        coluna_json.download_button(
            "Baixar relatório (JSON)", para_json(relatorio), file_name="auditoria.json"
        )
        coluna_markdown.download_button(
            "Baixar relatório (Markdown)", para_markdown(relatorio), file_name="auditoria.md"
        )
