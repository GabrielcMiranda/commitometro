from __future__ import annotations

from pathlib import Path

import streamlit as st

from commitometro.padroes import REGISTRO

st.set_page_config(page_title="Testador de ERs", page_icon="🧪")
st.title("Testador de Expressões Regulares")

chave = st.selectbox("Expressão regular", sorted(REGISTRO))
expressao = REGISTRO[chave]

st.subheader(f"{expressao.id} — {expressao.nome}")
st.write(f"**Finalidade:** {expressao.finalidade}")
st.write(f"**Alfabeto:** {expressao.alfabeto}")
st.write(f"**ER formal:** {expressao.formal}")
st.code(expressao.padrao, language="text")

caminho_afne = Path("docs/afne") / f"{expressao.id}.png"
if caminho_afne.exists():
    st.image(str(caminho_afne), caption=f"AFNε de {expressao.id}")
else:
    st.info(f"AFNε de {expressao.id} ainda não disponível em {caminho_afne}.")

cadeias_texto = st.text_area("Cadeias para testar (uma por linha)")

if st.button("Testar"):
    for linha in cadeias_texto.splitlines():
        correspondencia = expressao.compilada.fullmatch(linha)
        veredito = "✅ aceita" if correspondencia else "❌ rejeitada"
        st.write(f"`{linha}` → {veredito}")
