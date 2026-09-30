# Roteiro da apresentação — Commitômetro

Duração alvo: ≈ 11 minutos de fala + perguntas. Cada integrante defende 2 ERs e o que
construiu, para que os três demonstrem domínio do trabalho inteiro, não só da própria parte.

## Slides, falas e tempos

| # | Slide | Quem fala | Tempo |
|---|---|---|---|
| 1 | Capa: projeto e equipe | A | 0:15 |
| 2 | Problema: convenções no Git (histórico bagunçado × organizado) | A | 0:45 |
| 3 | Solução: entrada → processamento → saída, arquitetura e stack | B | 0:45 |
| 4 | Notação: ER formal × sintaxe Python, `fullmatch`, sem `\d`/flags | A | 0:35 |
| 5 | Construção dos AFNε: Thompson, arcos por classe, legenda | C | 0:35 |
| 6 | ER-01 Cabeçalho: ficha resumida (formal × código) + AFNε em blocos | A | 0:55 |
| 7 | ER-02 Rodapé/BREAKING CHANGE + AFNε | A | 0:35 |
| 8 | ER-03 Versão semântica + AFNε **+ simulação: `1.0.0` aceita, `01.0.0` rejeitada** (ε-fecho passo a passo) | B | 1:05 |
| 9 | ER-04 Branch + AFNε | B | 0:35 |
| 10 | ER-05 Referência a issue + AFNε | C | 0:45 |
| 11 | ER-06 Coautoria (incluindo coautoria de IA) + AFNε | C | 0:45 |
| 12 | Regras de negócio: conformidade por autor e sugestão de versão | B | 0:35 |
| 13 | **Demonstração ao vivo — CLI e Streamlit** (roteiro abaixo) | C | 1:40 |
| 14 | Testes, equivalência AFNε × ER, limitações e melhorias | A | 0:45 |
| 15 | Contribuições de cada integrante | B | 0:25 |

Totais: A ≈ 3:50 · B ≈ 3:25 · C ≈ 3:45.

## Falas-chave por slide

- **1 — Capa:** nome do projeto, disciplina, os três integrantes.
- **2 — Problema:** commits sem convenção viram histórico ilegível; convenções existem
  (Conventional Commits, SemVer) mas raramente são checadas automaticamente. Mostrar um
  histórico "bagunçado" ao lado de um organizado.
- **3 — Solução:** diagrama de módulos (seção 4.2 do relatório) e o fluxo entrada →
  processamento → saída; por que GitPython/PyDriller, Typer, Rich, Streamlit.
- **4 — Notação:** por que `fullmatch` (não `search`/`^$`), por que nenhuma ER usa `\d`/`\w`
  nem *flags* — para casar exatamente com a ER formal escrita por extenso.
- **5 — AFNε:** construção de Thompson fragmento a fragmento; um arco de classe (`A` =
  `[a-z0-9]`) abrevia dezenas de arcos paralelos; cada ER tem sua legenda.
- **6/7 — ER-01/ER-02:** ficha resumida, formal ao lado do código, AFNε em blocos.
- **8 — ER-03:** ficha + AFNε + a simulação passo a passo de `1.0.0` (aceita) e `01.0.0`
  (rejeitada por zero à esquerda) — é o momento de abrir
  `docs/afne/simulacoes/ER-03_passo_a_passo.md` ou repetir a simulação ao vivo no JFLAP se o
  professor pedir.
- **9/10/11 — ER-04/ER-05/ER-06:** ficha + AFNε de cada uma; destacar em ER-06 a extensão
  para coautoria de IA, motivada por um caso real do próprio histórico do projeto.
- **12 — Regras de negócio:** como a conformidade por autor é calculada e como a próxima
  versão é sugerida a partir dos tipos de commit desde a última tag.
- **13 — Demonstração ao vivo:** ver roteiro abaixo.
- **14 — Testes e limitações:** 111 casos oficiais + 12 000 cadeias aleatórias sem
  divergência entre AFNε e ER; cobertura de 98,59%; limitações documentadas por ER (seção 9
  do relatório).
- **15 — Contribuições:** tabela de quem fez o quê (seção 10 do relatório /
  `CONTRIBUICOES.md`).

