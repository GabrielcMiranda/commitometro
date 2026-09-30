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
