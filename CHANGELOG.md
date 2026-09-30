# Changelog

Todas as mudanças notáveis deste projeto são documentadas neste arquivo.

## [1.0.0]

Primeira versão completa do Commitômetro, entregue como trabalho da disciplina de
Linguagens Formais e Autômatos.

### Adicionado

- As 6 expressões regulares do projeto (`ER-01` a `ER-06`), cobrindo cabeçalho de commit,
  linha de rodapé (`BREAKING CHANGE`), tag de versão semântica, nome de branch, referência
  a issue e linha de coautoria — esta última já preparada para coautoria de assistentes de
  IA, um caso real observado no próprio histórico do projeto.
- Leitura do histórico a partir de um repositório Git local (GitPython + PyDriller) ou de
  arquivos exportados (`git log` com separadores de campo/registro).
- Análise de cada commit: tipo, escopo, quebra de compatibilidade, issues e coautores
  extraídos do corpo da mensagem, com diagnóstico legível para cabeçalhos rejeitados.
- Cálculo de conformidade por autor, classificação de branches e tags, e sugestão da
  próxima versão semântica (maior, menor, correção ou pré-lançamento) a partir dos tipos
  de commit registrados desde a última tag estável.
- Relatório de auditoria em três formatos: tabela colorida (Rich), JSON e Markdown.
- CLI (`commitometro auditar`, `validar`, `versao`, `ers`) com mensagens de erro claras
  para entradas vazias ou inválidas, sem traceback.
- Interface web em Streamlit: página de auditoria (upload ou caminho local, métricas,
  gráfico e download do relatório) e testador interativo das 6 ERs.
- CI no GitHub Actions com testes (Python 3.12 e 3.13), cobertura mínima de 85% e
  autoauditoria das mensagens de commit do próprio repositório em cada PR.
- Documentação completa: ficha de cada ER em `docs/ers/`, `docs/EXPRESSOES.md` gerado
  automaticamente a partir do código, análise de resultados dos casos de teste, dados de
  exemplo e um gerador de repositório de demonstração.

### Conhecido

- `ER-06` rejeita nomes de conta de bot com colchetes (ex.: `dependabot[bot]`).
- `ER-05` exige que o dono/repositório de uma referência cruzada esteja em minúsculas.
- `ER-02` não valida os trailers contra uma lista fechada de nomes reconhecidos.
- `ER-01` não limita o cabeçalho a 72 caracteres.

Ver [`resultados/ANALISE_RESULTADOS.md`](resultados/ANALISE_RESULTADOS.md) para a lista
completa de casos testados e a cobertura da suíte.

## [0.1.0]

- As 6 expressões regulares implementadas, registradas e testadas (Etapa 2 do plano de
  implementação), congelando a especificação usada pelo restante do projeto.
