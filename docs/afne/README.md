# Convenção dos AFNε

## Método de construção

Todos os 6 AFNε são construídos pela **construção de Thompson** (ER → AFNε), a mesma da
disciplina: um fragmento por operador (literal, concatenação, união, fecho de Kleene,
opcional, fecho positivo), combinados de baixo para cima seguindo a **ER formal** de cada
ficha em `docs/ers/`.

Os `.jff` deste projeto foram gerados por um construtor de Thompson em Python (ver
`scripts/afne.py` para o simulador que os lê), em vez de desenhados diretamente na
interface do JFLAP — o algoritmo aplicado é exatamente o mesmo. **O que ainda depende de
abrir o JFLAP:** carregar cada `.jff`, rodar *View → Apply a Special Layout* pra organizar
visualmente, e exportar o PNG (`File → Save Image As…`). Isso é descrito arquivo por
arquivo nos `README` de entrega.

## Regras

1. **Um único estado inicial**; estados finais marcados explicitamente. Nas uniões, fechos
   e opcionais, os ε de entrada/saída do fragmento ficam sempre visíveis — só o ε que liga
   dois fragmentos **concatenados em sequência** pode ser omitido no diagrama final (mas
   ele existe no `.jff`; é só visualmente redundante).
2. **Arcos rotulados por classe:** um arco rotulado com um símbolo de classe (ex.: `A`)
   abrevia a união de todos os caracteres daquele conjunto (ex.: `A` = `[a-z0-9]` abrevia
   36 arcos paralelos). Isso é dito explicitamente no relatório e nos slides.
3. **Símbolos de classe não colidem com literais daquela ER.** Cada ER tem sua própria
   tabela de símbolos, documentada na legenda (`ER-0X.legenda.json`) e na tabela abaixo.
4. **Espaço:** o caractere real `' '` é representado no JFLAP pelo símbolo `_`.
5. **Exceção da ER-03** (usada na demonstração ao vivo): os dígitos são dois arcos
   separados, `0` e `P` (= `[1-9]`), nunca uma classe genérica `D`. Isso torna a tradução
   cadeia-real → cadeia-representativa um homomorfismo exato, sem ambiguidade quando o
   professor dita uma versão.

## Formato da legenda (`ER-0X.legenda.json`)

```json
{
  "id": "ER-01",
  "espaco": "_",
  "classes": {
    "A": {"intervalos": [["a", "z"], ["0", "9"]]},
    "N": {"exceto": ["\n", " "]},
    "C": {"exceto": ["\n"]}
  }
}
```
- `"espaco"`: símbolo do JFLAP que representa o caractere `' '` real.
- `"classes"`: símbolo → predicado. `"intervalos"` é uma lista de `[inicio, fim]`
  (inclusive nos dois lados); `"exceto"` é um conjunto de caracteres proibidos (o resto de
  Σ é aceito); `"conjunto"` é uma lista literal de caracteres aceitos.
- Qualquer símbolo de arco que **não** apareça em `"classes"` nem seja `"espaco"` é tratado
  como o próprio caractere literal.
- Rótulo de transição vazio (`<read/>`) é sempre ε.

`scripts/afne.py` (Etapa 1.2) implementa exatamente essa semântica para simular qualquer
`.jff` + legenda contra uma cadeia real.

## Tradução cadeia real → cadeia representativa

Como os arcos são rotulados por classe, o JFLAP simula uma **cadeia representativa** sobre
o alfabeto abstrato (literais + símbolos de classe), não a cadeia real diretamente.
Exemplo, ER-01: `fix(auth): ok` → `fix(AAAA):_NC` (cada letra de `auth` casa com a classe
`A`, o espaço vira `_`, e o resto do corpo casa com `N` depois `C`). Pra simular no JFLAP
(*Input → Step with Closure* ou *Multiple Run*), traduzam a cadeia real assim antes de
digitar. A equivalência sobre as **cadeias reais** (sem precisar traduzir à mão) é quem
garante `scripts/afne.py`, usado no teste de equivalência da Etapa 3.

## Tabela de símbolos de classe por ER

| ER | Literais que os símbolos não podem colidir | Símbolos de classe |
|---|---|---|
| ER-01 | letras minúsculas dos 11 tipos, `( ) ! :` | `A` = `[a-z0-9]` · `N` = C₀ · `C` = C |
| ER-02 | letras de `BREAKING CHANGE`, `- : #` | `L` = letra · `x` = C₀ · `y` = C |
| ER-03 | `v`, `alpha`, `beta`, `rc`, `. -` | `P` = `[1-9]` (nunca uma classe `D` genérica — ver regra 5) |
| ER-04 | letras minúsculas de `main/develop/feature/...`, `/` | `A` = `[a-z0-9]` (mesma da ER-01); reaproveita o sub-AFNε de N da ER-03 |
| ER-05 | letras de `close/fix/resolve/refs` (minúsculas e maiúsculas `C F R`) | `O` = `[a-z0-9-]` · `Q` = `O ∪ {., _}` (evita colidir com o literal `R`) · `P` = `[1-9]` |
| ER-06 | `C A a B b`, `.` | `1` = L (letra) · `5` = D (dígito) · `2` = U · `3` = H · `4` = Z |

Os símbolos de classe usam dígitos na ER-06 porque **todas** as letras (maiúsculas e
minúsculas) já são literais em `Co-Authored-By`.
