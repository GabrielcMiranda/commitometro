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

## 5. Expressões regulares

## 6. Autômatos finitos com movimentos vazios (AFNε)

## 7. Testes e análise dos resultados

## 8. Resultados da aplicação

## 9. Limitações e melhorias

## 10. Contribuições

## 11. Conclusão

## Referências

## Apêndices
