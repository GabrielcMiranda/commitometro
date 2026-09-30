# Expressões regulares do Commitômetro

Gerado automaticamente por `scripts/gerar_docs_ers.py` a partir do `REGISTRO`; não editar à mão.

## ER-01 — Cabeçalho de commit (Conventional Commits)

- **Finalidade:** Validar a 1ª linha do commit no formato tipo(escopo)!: descrição e extrair tipo, escopo e marca de quebra.
- **Alfabeto:** Σ = caracteres Unicode; T = feat | fix | docs | style | refactor | perf | test | build | ci | chore | revert; A = {a,…,z} ∪ {0,…,9}; C = Σ − {\n}; C₀ = C − {␣}.
- **ER formal:** `T ( '(' A A* ( - A A* )* ')' | ε ) ( ! | ε ) :␣ C₀ C*`
- **Sintaxe implementada:**
  ```python
  r"(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(([a-z0-9]+(-[a-z0-9]+)*)\))?(!?): ([^ \n][^\n]*)"
  ```
- **Grupos:**
  - 1: tipo
  - 3: escopo
  - 5: marca de quebra (! ou vazio)
  - 6: descrição

## ER-02 — Linha de rodapé (trailer)

- **Finalidade:** Reconhecer linhas de rodapé do Conventional Commits/git trailers e detectar BREAKING CHANGE.
- **Alfabeto:** L = {A,…,Z} ∪ {a,…,z}; W = L L*; C e C₀ como na ER-01.
- **ER formal:** `( BREAKING␣CHANGE | W ( - W )* ) ( :␣ | ␣# ) C₀ C*`
- **Sintaxe implementada:**
  ```python
  r"(BREAKING CHANGE|[A-Za-z]+(-[A-Za-z]+)*)(: | #)([^ \n][^\n]*)"
  ```
- **Grupos:**
  - 1: token
  - 3: separador
  - 4: valor

## ER-03 — Tag de versão semântica

- **Finalidade:** Reconhecer tags SemVer, com ou sem v e com pré-lançamento opcional, para ordenar versões e sugerir a próxima.
- **Alfabeto:** D = {0,…,9}; P = D − {0}; N = 0 | P D* (número sem zero à esquerda).
- **ER formal:** `( v | ε ) N '.' N '.' N ( - ( alpha | beta | rc ) ( '.' N | ε ) | ε )`
- **Sintaxe implementada:**
  ```python
  r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-(alpha|beta|rc)(\.(0|[1-9][0-9]*))?)?"
  ```
- **Grupos:**
  - 1: maior
  - 2: menor
  - 3: correção
  - 5: rótulo de pré-lançamento
  - 7: número do pré-lançamento

## ER-04 — Nome de branch

- **Finalidade:** Verificar se as branches seguem o fluxo main/develop + prefixos.
- **Alfabeto:** A = {a,…,z} ∪ {0,…,9}; S = A A* ( - A A* )*; N como na ER-03.
- **ER formal:** `main | develop | ( feature | bugfix | hotfix | docs ) / S | release / N '.' N '.' N`
- **Sintaxe implementada:**
  ```python
  r"main|develop|(feature|bugfix|hotfix|docs)/[a-z0-9]+(-[a-z0-9]+)*|release/(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
  ```
- **Grupos:**
  - 1: prefixo (feature/bugfix/hotfix/docs)
  - 3: maior de release
  - 4: menor de release
  - 5: correção de release

## ER-05 — Referência a issue

- **Finalidade:** Encontrar linhas que fecham ou referenciam issues (palavras-chave do GitHub), inclusive de outro repositório.
- **Alfabeto:** K = (C|c)lose(s|d|ε) | (F|f)ix(es|ed|ε) | (R|r)esolve(s|d|ε) | (R|r)efs; O = {a,…,z} ∪ {0,…,9} ∪ {-}; R = O ∪ {., _}; D, P como na ER-03; I = ( O O* / R R* | ε ) # P D*.
- **ER formal:** `K ( : | ε ) ␣ I ( ,␣ I )*`
- **Sintaxe implementada:**
  ```python
  r"([Cc]lose[sd]?|[Ff]ix(es|ed)?|[Rr]esolve[sd]?|[Rr]efs):? ([a-z0-9-]+/[a-z0-9._-]+)?#[1-9][0-9]*(, ([a-z0-9-]+/[a-z0-9._-]+)?#[1-9][0-9]*)*"
  ```
- **Grupos:**
  - 1: palavra-chave

## ER-06 — Linha de coautoria

- **Finalidade:** Reconhecer Co-authored-by e extrair nome e e-mail do coautor para creditar a contribuição, inclusive de assistentes de IA.
- **Alfabeto:** L = {A,…,Z} ∪ {a,…,z} ∪ {À,…,Ö} ∪ {Ø,…,ö} ∪ {ø,…,ÿ}; D = {0,…,9}; M = L ∪ D; T = M M* ( '.' M M* | ε ); U = {A,…,Z,a,…,z,0,…,9} ∪ {., _, '+', -}; H = {A,…,Z,a,…,z,0,…,9} ∪ {-}; Z = {A,…,Z} ∪ {a,…,z}.
- **ER formal:** `Co-(A|a)uthored-(B|b)y:␣ T (␣ T)* ␣< U U* @ H H* ( '.' H H* )* '.' Z Z* >`
- **Sintaxe implementada:**
  ```python
  r"Co-[Aa]uthored-[Bb]y: ([A-Za-zÀ-ÖØ-öø-ÿ0-9]+(\.[A-Za-zÀ-ÖØ-öø-ÿ0-9]+)?( [A-Za-zÀ-ÖØ-öø-ÿ0-9]+(\.[A-Za-zÀ-ÖØ-öø-ÿ0-9]+)?)*) <([A-Za-z0-9._+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]+)>"
  ```
- **Grupos:**
  - 1: nome completo
  - 5: e-mail

