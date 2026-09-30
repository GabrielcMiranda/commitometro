from __future__ import annotations

from pathlib import Path

from commitometro.padroes import REGISTRO

CAMINHO_SAIDA = Path("docs/EXPRESSOES.md")


def gerar() -> str:
    partes = [
        "# Expressões regulares do Commitômetro",
        "",
        "Gerado automaticamente por `scripts/gerar_docs_ers.py` a partir do `REGISTRO`; "
        "não editar à mão.",
        "",
    ]
    for chave in sorted(REGISTRO):
        expressao = REGISTRO[chave]
        partes.append(f"## {expressao.id} — {expressao.nome}")
        partes.append("")
        partes.append(f"- **Finalidade:** {expressao.finalidade}")
        partes.append(f"- **Alfabeto:** {expressao.alfabeto}")
        partes.append(f"- **ER formal:** `{expressao.formal}`")
        partes.append("- **Sintaxe implementada:**")
        partes.append("  ```python")
        partes.append(f'  r"{expressao.padrao}"')
        partes.append("  ```")
        if expressao.grupos:
            partes.append("- **Grupos:**")
            for indice, descricao in sorted(expressao.grupos.items()):
                partes.append(f"  - {indice}: {descricao}")
        partes.append("")
    return "\n".join(partes) + "\n"


if __name__ == "__main__":
    CAMINHO_SAIDA.write_text(gerar(), encoding="utf-8")
    print(f"Documentação gerada em {CAMINHO_SAIDA}")
