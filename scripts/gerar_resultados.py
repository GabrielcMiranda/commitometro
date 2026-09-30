from __future__ import annotations

import json
from pathlib import Path

from commitometro.padroes import REGISTRO

_ARQUIVO_DE_CASOS = {
    "ER-01": "er01_cabecalho.json",
    "ER-02": "er02_rodape.json",
    "ER-03": "er03_versao.json",
    "ER-04": "er04_branch.json",
    "ER-05": "er05_referencia.json",
    "ER-06": "er06_coautoria.json",
}

_LIMITACOES_CONHECIDAS = {
    "ER-01": "não limita o tamanho do cabeçalho a 72 caracteres, como recomenda a convenção.",
    "ER-02": "aceita qualquer token formado só por letras como se fosse um trailer válido, "
    "mesmo que não seja um nome reconhecido (ex.: git não valida 'Xyz-by:').",
    "ER-05": "exige que o dono/repositório de uma referência cruzada esteja em minúsculas, "
    "então 'Org/Repo#3' é rejeitado mesmo sendo um link válido no GitHub.",
    "ER-06": "rejeita contas de bot com colchetes no nome, como 'dependabot[bot]', "
    "porque o alfabeto do nome não inclui '[' nem ']'.",
}

DIRETORIO_CASOS = Path("tests/casos")
CAMINHO_COVERAGE = Path("coverage.json")
CAMINHO_SAIDA = Path("resultados/ANALISE_RESULTADOS.md")


def _avaliar_er(chave: str) -> tuple[list[dict], int, int]:
    expressao = REGISTRO[chave]
    dados = json.loads((DIRETORIO_CASOS / _ARQUIVO_DE_CASOS[chave]).read_text(encoding="utf-8"))
    linhas = []
    acertos = 0
    total = 0
    for esperado, grupo in (("aceita", dados["aceitas"]), ("rejeitada", dados["rejeitadas"])):
        for caso in grupo:
            total += 1
            obtido = "aceita" if expressao.compilada.fullmatch(caso["cadeia"]) else "rejeitada"
            certo = obtido == esperado
            acertos += certo
            linhas.append(
                {
                    "cadeia": caso["cadeia"],
                    "esperado": esperado,
                    "obtido": obtido,
                    "limite": caso.get("limite", False),
                    "motivo": caso.get("motivo", ""),
                    "certo": certo,
                }
            )
    return linhas, acertos, total


def _linha_de_cobertura() -> str:
    if not CAMINHO_COVERAGE.exists():
        return (
            "_Cobertura não incluída: rode `pytest --cov=commitometro --cov-report=json` "
            "antes de gerar este relatório._"
        )
    dados = json.loads(CAMINHO_COVERAGE.read_text(encoding="utf-8"))
    percentual = dados["totals"]["percent_covered"]
    return f"Cobertura total da suíte: **{percentual:.2f}%**."


def gerar() -> str:
    partes = ["# Análise de resultados", ""]
    total_geral = 0
    acertos_geral = 0

    for chave in sorted(REGISTRO):
        linhas, acertos, total = _avaliar_er(chave)
        total_geral += total
        acertos_geral += acertos
        partes.append(f"## {chave} — {acertos}/{total} casos corretos")
        partes.append("")
        partes.append("| Cadeia | Esperado | Obtido | Limite | Motivo |")
        partes.append("|---|---|---|---|---|")
        for linha in linhas:
            marcador = "" if linha["certo"] else " ⚠️"
            partes.append(
                f"| `{linha['cadeia']}` | {linha['esperado']} | {linha['obtido']}{marcador} | "
                f"{'sim' if linha['limite'] else 'não'} | {linha['motivo']} |"
            )
        partes.append("")

    partes.append(f"**Total geral:** {acertos_geral}/{total_geral} casos corretos.")
    partes.append("")
    partes.append(_linha_de_cobertura())
    partes.append("")
    partes.append("## Limitações conhecidas")
    partes.append("")
    for chave, texto in _LIMITACOES_CONHECIDAS.items():
        partes.append(f"- **{chave}** {texto}")
    partes.append("")

    return "\n".join(partes) + "\n"


if __name__ == "__main__":
    CAMINHO_SAIDA.parent.mkdir(exist_ok=True)
    CAMINHO_SAIDA.write_text(gerar(), encoding="utf-8")
    print(f"Análise gerada em {CAMINHO_SAIDA}")
