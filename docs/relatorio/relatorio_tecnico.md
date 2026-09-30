<link rel="stylesheet" href="estilo.css">

<div class="capa">

<div class="instituicao">
Disciplina de Linguagens Formais e Autômatos
</div>

# Commitômetro

## Auditor de Convenções de Commits e Versionamento em Repositórios Git, baseado em Expressões Regulares e Autômatos Finitos

Relatório técnico

Gabriel Miranda · Yago Schnorr · João Pedro Silva

<div class="data">
2026
</div>

</div>

## Sumário

1. [Resumo](#1-resumo)
2. [Introdução](#2-introdução)
3. [Fundamentação teórica](#3-fundamentação-teórica)
4. [Arquitetura e implementação](#4-arquitetura-e-implementação)
5. [Expressões regulares](#5-expressões-regulares)
6. [Autômatos finitos com movimentos vazios (AFNε)](#6-autômatos-finitos-com-movimentos-vazios-afnε)
7. [Testes e análise dos resultados](#7-testes-e-análise-dos-resultados)
8. [Resultados da aplicação](#8-resultados-da-aplicação)
9. [Limitações e melhorias](#9-limitações-e-melhorias)
10. [Contribuições](#10-contribuições)
11. [Conclusão](#11-conclusão)
- [Referências](#referências)
- [Apêndices](#apêndices)

## 1. Resumo

## 2. Introdução

Repositórios Git colaborativos dependem de convenções — como as mensagens de commit
padronizam a comunicação entre quem escreve o código e quem lê o histórico depois (revisor,
gerador de changelog, ferramenta de CI). Na prática, porém, essas convenções raramente são
verificadas de forma automática e sistemática: cada integrante segue o padrão "de memória",
e desvios só são percebidos quando já causaram um problema (um changelog manual, uma tag de
versão fora de ordem, uma issue nunca fechada porque a palavra-chave foi digitada errado).

O Commitômetro nasce dessa lacuna. Ele lê o histórico de um repositório Git — local, via
`GitPython`/`PyDriller`, ou exportado em arquivo de log, para auditar repositórios sem
acesso direto — e usa **seis expressões regulares** para validar, em cada commit, cinco
aspectos distintos:

1. o cabeçalho da mensagem, no formato Conventional Commits (ER-01);
2. as linhas de rodapé (trailers), incluindo marcação de quebra de compatibilidade (ER-02);
3. tags de versão semântica, para ordenar releases e sugerir a próxima versão (ER-03);
4. nomes de branch, quanto ao fluxo `main`/`develop` e prefixos convencionais (ER-04);
5. referências e fechamento de issues (ER-05) e linhas de coautoria (ER-06).

O objetivo do trabalho, no contexto da disciplina, é duplo: entregar uma ferramenta que
realmente resolve esse problema de auditoria, e demonstrar de ponta a ponta a relação entre
**expressão regular**, **autômato finito com movimentos vazios (AFNε)** e **implementação em
código** — a mesma cadeia de equivalências estudada em Linguagens Formais e Autômatos,
aplicada a um problema real e não a um exercício isolado.

**Escopo:** o Commitômetro audita convenções sintáticas verificáveis por expressão regular
sobre uma única linha (ou um pequeno conjunto delas) de cada commit; não avalia qualidade de
código, tamanho de diff, nem semântica da mudança. As seis expressões regulares e suas
implementações em `src/commitometro/padroes/` são o núcleo da auditoria; o restante do
pacote (leitores de repositório, cálculo de conformidade, sugestão de versão, relatório,
CLI e interface web) existe para tornar esse núcleo utilizável em um fluxo de trabalho real.

## 3. Fundamentação teórica

### 3.1 Linguagens regulares e expressões regulares

Uma **linguagem regular** sobre um alfabeto Σ é qualquer linguagem que pode ser descrita por
uma **expressão regular (ER)** construída a partir de símbolos de Σ e da cadeia vazia ε,
combinados pelos três operadores regulares — **união** (`|`), **concatenação** (justaposição)
e **fecho de Kleene** (`*`, zero ou mais repetições) — e fechada sob agrupamento com
parênteses. Dois operadores derivados usados neste trabalho são abreviações desses três:
`r?` (opcional) equivale a `(r | ε)`, e `r+` (fecho positivo, uma ou mais repetições) equivale
a `r r*`. Classes de caracteres como `[a-z0-9]` ou `[^ \n]` são igualmente abreviações: a
primeira é a união de cada caractere do intervalo, a segunda a união de todo símbolo do
alfabeto exceto os listados — nenhuma delas amplia o poder expressivo além dos três
operadores regulares.

Por definição, o motor de expressões regulares do Python (módulo `re`) também oferece
recursos que **não são regulares** em sentido formal — retrorreferências (`\1`) e
*lookaround* (`(?=...)`, `(?<=...)`) — porque exigem memória além de um número finito de
estados (retrorreferência) ou verificação sem consumo que pode depender de contexto
arbitrariamente longo. Nenhuma das seis ERs deste projeto usa esses recursos: todas são
regulares em sentido estrito, o que é precondição para que cada uma tenha um AFNε
equivalente pela construção de Thompson (seção 3.3) — o que de fato acontece nas seis, como
mostra a seção 6.

### 3.2 Autômatos finitos com movimentos vazios (AFNε) e ε-fecho

Um **autômato finito não determinístico com movimentos vazios (AFNε)** é uma 5-upla
`M = (Q, Σ, δ, q₀, F)`, em que `Q` é um conjunto finito de estados, `Σ` o alfabeto, `q₀ ∈ Q`
o estado inicial, `F ⊆ Q` o conjunto de estados finais, e `δ: Q × (Σ ∪ {ε}) → 2^Q` a função
de transição — que, diferente de um AFD, pode levar um mesmo par (estado, símbolo) a vários
estados destino, e admite transições rotuladas por `ε` que não consomem símbolo de entrada.

A simulação de um AFNε usa o **ε-fecho** de um conjunto de estados: todo estado alcançável a
partir dele usando zero ou mais transições `ε`. O algoritmo de aceitação (o mesmo
implementado em `scripts/afne.py`, seção 6) é: (1) começar no ε-fecho de `{q₀}`; (2) para
cada símbolo da cadeia de entrada, calcular o conjunto de estados alcançados por uma
transição rotulada por aquele símbolo a partir de qualquer estado do conjunto atual, e tomar
o ε-fecho desse conjunto; (3) aceitar a cadeia se, ao final, o conjunto de estados atual
intersecta `F`. A seção 7.2 mostra esse algoritmo passo a passo para a ER-03.

### 3.3 Construção de Thompson e o teorema de Kleene

A **construção de Thompson** converte qualquer expressão regular em um AFNε equivalente,
por indução na estrutura da ER: um fragmento com dois estados e uma transição rotulada para
cada símbolo literal ou ε; para concatenação, uma transição ε liga o final do primeiro
fragmento ao início do segundo; para união, um novo estado inicial e um novo estado final
são ligados por ε a cada fragmento alternativo; para o fecho de Kleene, um novo par
inicial/final é ligado por ε ao fragmento original tanto para permitir pular a repetição
quanto para repeti-la, mais um ε de volta ao início do fragmento. Cada fragmento tem
exatamente um estado inicial e um final, o que torna a composição sempre bem definida — é
essa disciplina que a seção 6 aplica às seis ERs deste projeto.

Isso é metade construtiva do **teorema de Kleene**: toda linguagem regular é reconhecida por
algum autômato finito, e todo autômato finito reconhece uma linguagem regular (a outra
metade, autômato → ER, usa eliminação de estados ou expressões regulares generalizadas, e não
é necessária aqui porque partimos sempre da ER, nunca do autômato). O teorema garante que
"ER formal" e "AFNε" não são apenas notações relacionadas, mas **descrevem exatamente a
mesma linguagem** — a regra central verificada empiricamente na seção 7.1 deste projeto, via
teste automatizado de equivalência.

### 3.4 As convenções auditadas

- **Conventional Commits 1.0.0** define o formato `tipo(escopo)!: descrição` para o
  cabeçalho de um commit (ER-01) e o uso de linhas de rodapé — incluindo `BREAKING CHANGE:`
  para mudanças que quebram compatibilidade (ER-02).
- **Semantic Versioning (SemVer) 2.0.0** define o formato `MAJOR.MINOR.PATCH` com
  pré-lançamento opcional para tags de versão (ER-03), e a regra de que um commit `feat`
  força incremento de `MINOR` e um `BREAKING CHANGE` força incremento de `MAJOR` — a regra
  usada por `commitometro versao` para sugerir a próxima versão.
- ***Git trailers*** (`git-interpret-trailers`) são as linhas `Chave: valor` no rodapé de uma
  mensagem de commit — mecanismo genérico do qual `BREAKING CHANGE`, `Closes`/`Refs` e
  `Co-authored-by` são casos específicos.
- **Palavras-chave de fechamento de issue do GitHub** (`closes`, `fixes`, `resolves` e suas
  variações de tempo verbal e maiúsculas/minúsculas) fecham automaticamente uma issue
  referenciada quando o commit é mesclado na branch padrão (ER-05).
- **Coautoria via trailer** (`Co-authored-by: Nome <email>`) credita mais de uma pessoa — ou,
  cada vez mais comum, mais de um agente, incluindo assistentes de IA — por um commit
  (ER-06); a nota de projeto em `docs/ers/ER-06.md` documenta a decisão de ampliar essa ER
  para aceitar esse caso real.

## 4. Arquitetura e implementação

### 4.1 Stack e justificativa

| Camada | Ferramenta | Por quê |
|---|---|---|
| Linguagem | Python 3.12+ | módulo `re` nativo, tipagem gradual, ecossistema de testes maduro |
| Leitura de repositório | GitPython, PyDriller | GitPython dá acesso direto a commits/branches/tags de um repositório local; PyDriller complementa a mineração de histórico quando é preciso percorrer commits com metadados já estruturados, sem reimplementar o parsing do `git log` |
| CLI | Typer | comandos tipados por assinatura de função, `--help` gerado automaticamente, validação de argumentos sem código extra |
| Saída no terminal | Rich | tabelas, cores e painéis legíveis para o relatório de auditoria no terminal |
| Interface web | Streamlit | páginas interativas (upload de arquivo, tabela, gráfico) sem escrever HTML/JS, adequado ao prazo da disciplina |
| Testes | pytest + pytest-cov | parametrização (`@pytest.mark.parametrize`) para rodar os mesmos casos de `tests/casos/*.json` contra ER, AFNε e CLI sem repetir código |

### 4.2 Diagrama de módulos

O pacote é organizado em quatro camadas, cada uma dependendo apenas das anteriores:

```
entrada (leitores/)              →  arquivo.py (log exportado) · repositorio.py (GitPython)
        ↓
modelos (modelos.py)             →  Commit, Branch, Tag (dataclasses imutáveis)
        ↓
processamento
  padroes/  (as 6 ERs, REGISTRO) →  commits.py · versionamento.py · referencias.py
  analise.py                     →  diagnóstico de uma mensagem de commit (usa padroes/)
  conformidade.py                →  agrega diagnósticos por autor
  versionamento.py (raiz)        →  ordena tags e sugere a próxima versão (usa padroes/versionamento.py)
  auditoria.py                   →  orquestra leitura → análise → conformidade → sugestão
        ↓
saída
  relatorio.py                   →  formata o resultado da auditoria (texto Rich, JSON, Markdown)
  cli.py                         →  comandos Typer (`auditar`, `validar`, `versao`, `ers`)
  app/Auditoria.py + app/pages/  →  interface Streamlit (auditoria + testador de ERs)
```

Um diagrama gráfico equivalente (`docs/relatorio/arquitetura.png`) é exportado à parte,
como imagem, para a versão em PDF — a fonte da verdade da divisão em camadas é o bloco
acima, versionado como texto.

### 4.3 Fluxo entrada → processamento → saída

1. **Entrada:** `leitores/repositorio.py` abre um repositório local com GitPython e extrai
   commits (sem merges, por padrão), branches e tags; `leitores/arquivo.py` lê o mesmo
   conjunto de um log exportado no formato descrito no `README.md` (campos separados por
   `%x1f`, commits por `%x1e`), para auditar um repositório sem acesso direto a ele.
2. **Processamento:** `auditoria.py` orquestra a chamada de `analise.py` (que aplica as
   ERs de `padroes/` a cada commit e monta um diagnóstico — tipo, escopo, quebra de
   compatibilidade, issues referenciadas, coautores, ou o motivo da rejeição),
   `conformidade.py` (agrega os diagnósticos por autor) e `versionamento.py` (ordena as tags
   existentes pela ER-03 e sugere a próxima versão a partir dos tipos de commit desde a
   última tag).
3. **Saída:** `relatorio.py` formata o resultado da auditoria em três formatos — texto Rich
   colorido para o terminal, JSON para consumo por outra ferramenta, Markdown para anexar a
   um PR ou a este próprio relatório; `cli.py` expõe isso via Typer; `app/` expõe o mesmo
   resultado em duas páginas Streamlit.

### 4.4 Formato do log exportado

Ver `README.md`, seção "Exportando o histórico de um repositório": cada commit vira um
registro com 5 campos (hash, autor, e-mail, data ISO 8601, mensagem completa) separados por
`%x1f` (separador de unidade), e os registros são separados por `%x1e` (separador de
registro) — escolha que evita qualquer ambiguidade com mensagens de commit multilinha ou que
contenham `\n`, vírgula ou ponto e vírgula.

### 4.5 CLI, interface web e tratamento de entradas inválidas

A CLI (Typer) expõe quatro comandos: `auditar` (repositório local ou arquivos exportados,
com saída em texto/JSON/Markdown e `--falhar-se-invalido` para uso em CI), `validar`
(testa uma cadeia contra uma ER específica pelo id), `versao` (só a sugestão de próxima
versão) e `ers` (lista as 6 ERs registradas, com a ER formal e a forma implementada em
código). A interface web (Streamlit) tem a página de auditoria (upload ou caminho local,
métricas, tabela por autor, gráfico e download do relatório) e a página **Testador de ERs**,
usada para testar uma entrada nova durante a apresentação sem precisar de um repositório.

Toda entrada inválida — caminho inexistente, arquivo vazio, id de ER desconhecido,
repositório sem nenhum commit — é tratada por `erros.py` e sai com uma mensagem clara e
código de saída 2, sem *traceback* exposto ao usuário.

### 4.6 Decisões de implementação

- **`re.fullmatch`, nunca `re.match` ou `re.search`:** cada ER deve validar a cadeia inteira
  (cabeçalho inteiro, tag inteira, nome de branch inteiro), não apenas um prefixo — usar
  `match`/`search` aceitaria sufixos inválidos que `fullmatch` rejeita corretamente (ver, por
  exemplo, o caso-limite `Closes #3,#4` da ER-05, rejeitado porque a vírgula sem espaço não
  fecha a alternativa repetida `( ,␣ I )*` para a cadeia inteira).
- **Sem `\d`, `\w`, `\s`:** todas as classes são escritas por extenso (`[0-9]`, `[a-z0-9]`,
  `[^ \n]`) para que a correspondência com a ER formal do guia (que define classes por
  extensão de conjunto, não por atalho Perl) seja direta e auditável — é o que a coluna
  "Equivalência (atalho → operador formal)" de cada ficha (seção 5) documenta.
- **Sem *flags* (`re.IGNORECASE`, `re.MULTILINE`, etc.):** manter o comportamento default do
  `re` (sensível a maiúsculas/minúsculas, `.` não casa `\n`) evita que uma *flag* introduza
  uma diferença de linguagem não visível na ER escrita — por exemplo, `re.IGNORECASE`
  tornaria a ER-01 equivalente a uma linguagem maior do que a ER formal documentada, que usa
  `T` como união de literais exatamente minúsculos.

## 5. Expressões regulares

## 6. Autômatos finitos com movimentos vazios (AFNε)

## 7. Testes e análise dos resultados

## 8. Resultados da aplicação

## 9. Limitações e melhorias

## 10. Contribuições

## 11. Conclusão

## Referências

## Apêndices
