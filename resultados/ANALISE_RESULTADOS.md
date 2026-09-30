# Análise de resultados

## ER-01 — 19/19 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `feat: adiciona recuperação de senha` | aceita | aceita | não |  |
| `fix(auth): corrige expiração do token` | aceita | aceita | não |  |
| `feat(api-v2)!: remove endpoint legado` | aceita | aceita | não |  |
| `refactor!: reorganiza módulos internos` | aceita | aceita | não |  |
| `ci(github-actions): adiciona cache do pip` | aceita | aceita | não |  |
| `docs: x` | aceita | aceita | sim | descrição de 1 símbolo |
| `revert: feat(login): desfaz alteração` | aceita | aceita | não |  |
| `test(er01): cobre escopo com hífen` | aceita | aceita | não |  |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `Feat: adiciona login` | rejeitada | rejeitada | não |  |
| `feat:adiciona login` | rejeitada | rejeitada | não |  |
| `feat(): escopo vazio` | rejeitada | rejeitada | não |  |
| `feat(Login): escopo maiúsculo` | rejeitada | rejeitada | não |  |
| `feature: tipo inexistente` | rejeitada | rejeitada | não |  |
| `fix(auth) : espaço antes dos dois-pontos` | rejeitada | rejeitada | não |  |
| `feat:  descrição iniciando com espaço` | rejeitada | rejeitada | sim | descrição não pode começar com espaço |
| `fix(-auth): hífen inicial no escopo` | rejeitada | rejeitada | não |  |
| `feat!(api): ordem invertida` | rejeitada | rejeitada | não |  |
| `feat: ` | rejeitada | rejeitada | sim | descrição vazia |

## ER-02 — 17/17 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `BREAKING CHANGE: remove suporte ao Python 3.11` | aceita | aceita | não |  |
| `BREAKING-CHANGE: altera o formato do relatório` | aceita | aceita | não |  |
| `Reviewed-by: Ana Souza` | aceita | aceita | não |  |
| `Refs: #123` | aceita | aceita | não |  |
| `Closes #42` | aceita | aceita | não |  |
| `Co-authored-by: Ana <ana@x.com>` | aceita | aceita | não |  |
| `Acked-by: x` | aceita | aceita | sim | valor de 1 símbolo |
| `Signed-off-by: Bia <bia@ufx.br>` | aceita | aceita | não |  |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `BREAKING CHANGE:sem espaço` | rejeitada | rejeitada | não |  |
| `breaking change: minúsculo com espaço` | rejeitada | rejeitada | sim | só o token exato BREAKING CHANGE pode ter espaço |
| `Reviewed by: Ana` | rejeitada | rejeitada | não |  |
| `-Token: valor` | rejeitada | rejeitada | não |  |
| `Token-: valor` | rejeitada | rejeitada | não |  |
| `Token:  valor` | rejeitada | rejeitada | não |  |
| `Token #` | rejeitada | rejeitada | não |  |
| `Closes#42` | rejeitada | rejeitada | não |  |

## ER-03 — 18/18 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `1.0.0` | aceita | aceita | não |  |
| `v2.1.0` | aceita | aceita | não |  |
| `0.0.0` | aceita | aceita | sim | menor versão possível |
| `2.1.0-beta.3` | aceita | aceita | não |  |
| `v10.20.30-rc` | aceita | aceita | não |  |
| `1.0.0-alpha.0` | aceita | aceita | não |  |
| `v0.1.0-rc.12` | aceita | aceita | não |  |
| `999.0.1` | aceita | aceita | não |  |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `1.0` | rejeitada | rejeitada | não |  |
| `01.0.0` | rejeitada | rejeitada | sim | zero à esquerda |
| `v1.0.0-` | rejeitada | rejeitada | não |  |
| `1.0.0-gamma` | rejeitada | rejeitada | não |  |
| `1.0.0-beta.01` | rejeitada | rejeitada | não |  |
| `V1.0.0` | rejeitada | rejeitada | não |  |
| `1.0.0.0` | rejeitada | rejeitada | não |  |
| `1.0.0-beta3` | rejeitada | rejeitada | não |  |
| `1.0.0-BETA` | rejeitada | rejeitada | não |  |

## ER-04 — 18/18 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `main` | aceita | aceita | não |  |
| `develop` | aceita | aceita | não |  |
| `feature/login` | aceita | aceita | não |  |
| `feature/42-recuperar-senha` | aceita | aceita | não |  |
| `bugfix/corrige-null` | aceita | aceita | não |  |
| `hotfix/a` | aceita | aceita | sim | sufixo de 1 símbolo |
| `release/1.4.0` | aceita | aceita | não |  |
| `docs/readme` | aceita | aceita | não |  |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `master` | rejeitada | rejeitada | não |  |
| `feature/` | rejeitada | rejeitada | sim | sufixo vazio |
| `feature/Login` | rejeitada | rejeitada | não |  |
| `feature/login--social` | rejeitada | rejeitada | não |  |
| `feature/login-` | rejeitada | rejeitada | não |  |
| `feat/login` | rejeitada | rejeitada | não |  |
| `release/1.4` | rejeitada | rejeitada | não |  |
| `release/v1.4.0` | rejeitada | rejeitada | não |  |
| `feature/login/extra` | rejeitada | rejeitada | não |  |

## ER-05 — 18/18 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `Closes #1` | aceita | aceita | sim | menor número válido |
| `fixes #42` | aceita | aceita | não |  |
| `Resolves #7, #8, #9` | aceita | aceita | não |  |
| `Refs: #123` | aceita | aceita | não |  |
| `closed octocat/hello-world#15` | aceita | aceita | não |  |
| `Fix #3, org/repo.js#4` | aceita | aceita | não |  |
| `resolve #10` | aceita | aceita | não |  |
| `fixed #2` | aceita | aceita | não |  |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `Closes #0` | rejeitada | rejeitada | sim | número não pode ter zero à esquerda nem ser 0 |
| `closes #012` | rejeitada | rejeitada | não |  |
| `Closes#12` | rejeitada | rejeitada | não |  |
| `closes 12` | rejeitada | rejeitada | não |  |
| `Fixing #3` | rejeitada | rejeitada | não |  |
| `CLOSES #3` | rejeitada | rejeitada | não |  |
| `Closes #3,#4` | rejeitada | rejeitada | não |  |
| `Closes org/#3` | rejeitada | rejeitada | não |  |
| `Refs #3, ` | rejeitada | rejeitada | não |  |

## ER-06 — 21/21 casos corretos

| Cadeia | Esperado | Obtido | Limite | Motivo |
|---|---|---|---|---|
| `Co-authored-by: Ana Souza <ana.souza@gmail.com>` | aceita | aceita | não |  |
| `Co-authored-by: João Pedro de Miranda <joao@ufx.edu.br>` | aceita | aceita | não |  |
| `Co-Authored-By: Bia <12345+bia@users.noreply.github.com>` | aceita | aceita | não |  |
| `Co-authored-by: A <a@b.co>` | aceita | aceita | sim | nome e domínio mínimos |
| `Co-authored-by: Élise Müller <elise_m@uni-x.de>` | aceita | aceita | não |  |
| `Co-authored-By: Rui Costa <RUI.COSTA@EMPRESA.COM.BR>` | aceita | aceita | não |  |
| `Co-authored-by: Maria Eduarda Lima <maria-lima@dominio-exemplo.com.br>` | aceita | aceita | não |  |
| `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` | aceita | aceita | não |  |
| `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` | aceita | aceita | sim | sufixo de nome com ponto e dois dígitos |
| `` | rejeitada | rejeitada | sim | cadeia vazia |
| `Co-authored-by: Ana Souza ana@x.com` | rejeitada | rejeitada | não |  |
| `Co-authored-by: Ana <ana@localhost>` | rejeitada | rejeitada | não |  |
| `Co-authored-by: <ana@x.com>` | rejeitada | rejeitada | não |  |
| `co-authored-by: Ana <ana@x.com>` | rejeitada | rejeitada | não |  |
| `Co-authored-by:Ana <ana@x.com>` | rejeitada | rejeitada | não |  |
| `Co-authored-by: Ana  Souza <ana@x.com>` | rejeitada | rejeitada | sim | dois espaços entre as palavras do nome |
| `Co-authored-by: Ana <ana@x.c0m>` | rejeitada | rejeitada | não |  |
| `Co-Authored-By: Claude 5.5.5 <noreply@anthropic.com>` | rejeitada | rejeitada | sim | dois pontos no mesmo token de nome |
| `Co-Authored-By: Claude 5. <noreply@anthropic.com>` | rejeitada | rejeitada | sim | ponto sem dígito depois |
| `Co-authored-by: Ana <ana@x.com> ` | rejeitada | rejeitada | sim | espaço após o fechamento > |
| `Co-authored-by: dependabot[bot] <bot@x.com>` | rejeitada | rejeitada | não |  |

**Total geral:** 111/111 casos corretos.

Cobertura total da suíte: **98.59%**.

## Limitações conhecidas

- **ER-01** não limita o tamanho do cabeçalho a 72 caracteres, como recomenda a convenção.
- **ER-02** aceita qualquer token formado só por letras como se fosse um trailer válido, mesmo que não seja um nome reconhecido (ex.: git não valida 'Xyz-by:').
- **ER-05** exige que o dono/repositório de uma referência cruzada esteja em minúsculas, então 'Org/Repo#3' é rejeitado mesmo sendo um link válido no GitHub.
- **ER-06** rejeita contas de bot com colchetes no nome, como 'dependabot[bot]', porque o alfabeto do nome não inclui '[' nem ']'.

