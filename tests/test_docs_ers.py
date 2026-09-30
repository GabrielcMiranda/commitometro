from pathlib import Path

from scripts.gerar_docs_ers import CAMINHO_SAIDA, gerar


def test_docs_expressoes_esta_atualizada() -> None:
    atual = Path(CAMINHO_SAIDA).read_text(encoding="utf-8")
    assert atual == gerar(), (
        "docs/EXPRESSOES.md está desatualizado; rode "
        "`python scripts/gerar_docs_ers.py` e commite o resultado."
    )
