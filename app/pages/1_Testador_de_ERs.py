from __future__ import annotations

import streamlit as st

from commitometro.padroes import REGISTRO

st.set_page_config(page_title="Testador de ERs", page_icon="🧪")
st.title("Testador de Expressões Regulares")

chave = st.selectbox("Expressão regular", sorted(REGISTRO))
expressao = REGISTRO[chave]

cadeias_texto = st.text_area("Cadeias para testar (uma por linha)")

if st.button("Testar"):
    for linha in cadeias_texto.splitlines():
        correspondencia = expressao.compilada.fullmatch(linha)
        veredito = "✅ aceita" if correspondencia else "❌ rejeitada"
        st.write(f"`{linha}` → {veredito}")
