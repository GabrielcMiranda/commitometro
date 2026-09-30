from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from commitometro.padroes import REGISTRO

_ARQUIVO_DE_CASOS = {
    "ER-01": "er01_cabecalho.json",
    "ER-02": "er02_rodape.json",
    "ER-03": "er03_versao.json",
    "ER-04": "er04_branch.json",
    "ER-05": "er05_referencia.json",
    "ER-06": "er06_coautoria.json",
}

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

def _carregar_casos_oficiais() -> None:
    caminho = Path("tests/casos") / _ARQUIVO_DE_CASOS[chave]
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    cadeias = [item["cadeia"] for item in dados["aceitas"] + dados["rejeitadas"]]
    st.session_state["cadeias_teste"] = "\n".join(cadeias)


st.button("Carregar casos de teste oficiais", on_click=_carregar_casos_oficiais)

cadeias_texto = st.text_area("Cadeias para testar (uma por linha)", key="cadeias_teste")

if st.button("Testar"):
    for linha in cadeias_texto.splitlines():
        correspondencia = expressao.compilada.fullmatch(linha)
        veredito = "✅ aceita" if correspondencia else "❌ rejeitada"
        st.write(f"`{linha}` → {veredito}")
