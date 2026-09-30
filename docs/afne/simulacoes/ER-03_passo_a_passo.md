# ER-03 — simulação passo a passo (ε-fecho)

Rastro do ε-NFA da ER-03 (versão semântica) para uma cadeia representativa aceita
(`1.0.0`) e uma rejeitada por zero à esquerda (`01.0.0`), estado por estado, replicando
o que se vê no JFLAP em *Input → Step with Closure*.

### Cadeia `1.0.0` (aceita)

| Passo | Símbolo lido | Estados alcançados (antes do ε-fecho) | ε-fecho |
|---|---|---|---|
| 0 | (início) | {q2} | {q0, q2, q3, q58, q60, q62} |
| 1 | 1 | {q61} | {q50, q52, q54, q56, q57, q61, q63, q64} |
| 2 | . | {q65} | {q65, q74, q76, q78} |
| 3 | 0 | {q75} | {q75, q79, q80} |
| 4 | . | {q81} | {q81, q90, q92, q94} |
| 5 | 0 | {q91} | {q46, q48, q49, q91, q95} |

Estado(s) final(is) alcançado(s) ao fim da cadeia: {q49} → aceita.

---

### Cadeia `01.0.0` (rejeitada)

| Passo | Símbolo lido | Estados alcançados (antes do ε-fecho) | ε-fecho |
|---|---|---|---|
| 0 | (início) | {q2} | {q0, q2, q3, q58, q60, q62} |
| 1 | 0 | {q59} | {q59, q63, q64} |
| 2 | 1 | {} | {} |

Conjunto de estados esvaziou antes do fim da cadeia: cadeia rejeitada.
