from __future__ import annotations

import streamlit as st

from commitometro.auditoria import auditar

st.set_page_config(page_title="Commitômetro — Auditoria", page_icon="✅")
st.title("Commitômetro")
st.caption("Auditor de Convenções de Commits e Versionamento em Repositórios Git")

caminho_repositorio = st.text_input("Caminho do repositório Git")

if st.button("Auditar"):
    relatorio = auditar(caminho_repositorio)
    st.success(f"Auditoria concluída: {len(relatorio.por_autor)} autor(es) analisado(s).")
