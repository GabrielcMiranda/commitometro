# Commitômetro

Auditor de Convenções de Commits e Versionamento em Repositórios Git.

Analisa o histórico de um repositório Git (ou um arquivo de log exportado) e usa expressões
regulares para validar mensagens de commit no padrão Conventional Commits, tags de
versionamento semântico, nomes de branches, referências a issues e linhas de coautoria.
Gera um relatório de conformidade por autor e sugere a próxima versão do projeto com base
nos tipos de alteração registrados.

Trabalho da disciplina de Linguagens Formais e Autômatos.

## Ambiente

Requer Python 3.12 ou mais novo.

```
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e . -r requirements-dev.txt
```

## Testes

```
pytest --cov=commitometro --cov-report=term-missing
```
