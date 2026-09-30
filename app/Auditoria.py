from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from commitometro.auditoria import auditar

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
    caminho_historico = _salvar_temporario(arquivo_historico, ".log") if arquivo_historico else None
    caminho_tags = _salvar_temporario(arquivo_tags, ".txt") if arquivo_tags else None
    caminho_branches = _salvar_temporario(arquivo_branches, ".txt") if arquivo_branches else None

    relatorio = auditar(
        caminho_repositorio,
        historico=caminho_historico,
        arquivo_tags=caminho_tags,
        arquivo_branches=caminho_branches,
    )
    st.success(f"Auditoria concluída: {len(relatorio.por_autor)} autor(es) analisado(s).")
