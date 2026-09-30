# Commitômetro

Auditor de Convenções de Commits e Versionamento em Repositórios Git.

Analisa o histórico de um repositório Git (ou um arquivo de log exportado) e usa expressões
regulares para validar mensagens de commit no padrão Conventional Commits, tags de
versionamento semântico, nomes de branches, referências a issues e linhas de coautoria.
Gera um relatório de conformidade por autor e sugere a próxima versão do projeto com base
nos tipos de alteração registrados.

Trabalho da disciplina de Linguagens Formais e Autômatos.

## Requisitos

- Python 3.12 ou mais novo
- Git instalado e disponível no PATH

## Instalação

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e . -r requirements-dev.txt
```

Isso instala o pacote em modo editável, com as dependências de execução (GitPython,
PyDriller, Typer, Rich, Streamlit) e de desenvolvimento (pytest, pytest-cov).

## Exportando o histórico de um repositório

Para auditar um repositório sem acesso direto a ele (ou para gerar um arquivo de exemplo),
exporte o histórico com:

```bash
git log --no-merges --pretty=format:"%H%x1f%an%x1f%ae%x1f%aI%x1f%B%x1e" > historico.log
git tag --list > tags.txt
git branch -a --format="%(refname:short)" > branches.txt
```

`%x1f` (separador de unidade) separa os campos de cada commit, e `%x1e` (separador de
registro) separa um commit do próximo — assim mensagens de commit com várias linhas não
quebram o parser.

## Uso — linha de comando

```powershell
# audita um repositório local
commitometro auditar caminho\para\o\repositorio

# audita a partir de arquivos exportados
commitometro auditar --arquivo historico.log --tags tags.txt --branches branches.txt

# escolhe o formato de saída e salva em arquivo
commitometro auditar . --formato json --saida resultados/auditoria.json
commitometro auditar . --formato markdown --saida resultados/auditoria.md

# inclui commits de merge (por padrão são ignorados)
commitometro auditar . --incluir-merges

# sai com código 1 se houver commit fora do padrão (usado no CI)
commitometro auditar . --falhar-se-invalido

# testa uma cadeia contra uma ER específica
commitometro validar er03 "2.1.0-beta.3"
commitometro validar er01 "feat(auth): adiciona login"

# só a sugestão da próxima versão
commitometro versao .
commitometro versao --arquivo historico.log --tags tags.txt --pre beta

# lista as 6 ERs registradas, com a forma formal e a do código
commitometro ers
commitometro ers --markdown
```

Toda entrada inválida (caminho inexistente, arquivo vazio, ER desconhecida, repositório sem
commits, etc.) mostra uma mensagem clara e sai com código 2, sem traceback.

![Saída de commitometro auditar dados/repo_demo](docs/imagens/cli_auditar.png)

![Saída de commitometro validar er03 "2.1.0-beta.3"](docs/imagens/cli_validar.png)

## Uso — interface web

```powershell
streamlit run app/Auditoria.py
```

Abre a página de auditoria (caminho local do repositório ou upload dos arquivos
exportados, com métricas, tabela por autor, gráfico de conformidade e download do
relatório em JSON/Markdown). A página **Testador de ERs**, acessível pelo menu lateral,
deixa testar qualquer uma das 6 ERs contra cadeias digitadas na hora — é a ferramenta
usada quando o professor pede para testar uma entrada nova durante a apresentação.

![Página de auditoria no Streamlit](docs/imagens/web_auditoria.png)

![Página Testador de ERs no Streamlit](docs/imagens/web_testador.png)

## Testes

```powershell
pytest --cov=commitometro --cov-report=term-missing
```

A suíte cobre as 6 ERs (com pelo menos 6 cadeias aceitas, 6 rejeitadas e 1 caso-limite
cada, em `tests/casos/`), os leitores de arquivo e de repositório, a análise de mensagens,
o cálculo de conformidade, a sugestão de versão, a orquestração da auditoria, o relatório
e a CLI. A cobertura mínima exigida no CI é 85%.

Para gerar um repositório de demonstração e testar os leitores contra dados reais:

```powershell
python scripts/gerar_repo_demo.py
```

Isso cria `dados/repo_demo/` (não é versionado — é só um artefato local).

## Estrutura do repositório

```
commitometro/
├── src/commitometro/       # pacote principal
│   ├── padroes/            # as 6 ERs (commits.py, versionamento.py, referencias.py)
│   ├── leitores/           # leitura de arquivo exportado e de repositório Git
│   ├── modelos.py          # dataclasses do domínio
│   ├── erros.py            # EntradaInvalidaError
│   ├── analise.py          # aplica as ERs a cada commit
│   ├── conformidade.py     # agrega por autor, classifica branches e tags
│   ├── versionamento.py    # sugere a próxima versão semântica
│   ├── auditoria.py        # orquestra tudo
│   ├── relatorio.py        # saída em tabela (Rich), JSON e Markdown
│   └── cli.py               # comandos Typer
├── app/                     # interface Streamlit
├── tests/                   # testes e casos de teste (tests/casos/*.json)
├── scripts/                  # geração de demo, resultados e documentação
├── dados/exemplos/           # histórico, tags e branches de exemplo
├── docs/ers/                 # ficha completa de cada ER
├── docs/EXPRESSOES.md         # documentação das ERs gerada a partir do código
└── resultados/                # cobertura, análise de resultados, autoauditoria
```

## As 6 expressões regulares

| ID | Nome | Ficha |
|---|---|---|
| ER-01 | Cabeçalho de commit (Conventional Commits) | [docs/ers/ER-01.md](docs/ers/ER-01.md) |
| ER-02 | Linha de rodapé / trailer (inclui `BREAKING CHANGE`) | [docs/ers/ER-02.md](docs/ers/ER-02.md) |
| ER-03 | Tag de versão semântica | [docs/ers/ER-03.md](docs/ers/ER-03.md) |
| ER-04 | Nome de branch | [docs/ers/ER-04.md](docs/ers/ER-04.md) |
| ER-05 | Referência a issue | [docs/ers/ER-05.md](docs/ers/ER-05.md) |
| ER-06 | Linha de coautoria (inclusive de assistentes de IA) | [docs/ers/ER-06.md](docs/ers/ER-06.md) |

A documentação em [docs/EXPRESSOES.md](docs/EXPRESSOES.md) é gerada automaticamente a
partir do código (`python scripts/gerar_docs_ers.py`), então o padrão documentado é sempre
byte a byte o mesmo do código-fonte.

## Declaração de uso de IA

A equipe usou o Claude (Anthropic) como apoio em partes pontuais do trabalho: implementação
e testes das seis ERs, geração dos diagramas dos AFNε, montagem dos slides da apresentação e
automação na criação de issues no GitHub. Todo o conteúdo produzido foi revisado e é
compreendido e defendido pela equipe.

## Créditos e referências

- [GitPython](https://gitpython.readthedocs.io/) e [PyDriller](https://pydriller.readthedocs.io/) — leitura do histórico Git
- [Typer](https://typer.tiangolo.com/) e [Rich](https://rich.readthedocs.io/) — interface de linha de comando
- [Streamlit](https://streamlit.io/) — interface web
- [pytest](https://docs.pytest.org/) e [pytest-cov](https://pytest-cov.readthedocs.io/) — testes e cobertura
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [git-interpret-trailers](https://git-scm.com/docs/git-interpret-trailers)
- Documentação do GitHub sobre [palavras-chave de fechamento de issues](https://docs.github.com/pt/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) e [commits com coautoria](https://docs.github.com/pt/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors)
