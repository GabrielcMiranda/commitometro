from __future__ import annotations

from commitometro.modelos import AnaliseCommit, Commit
from commitometro.padroes.commits import Rodape, validar_cabecalho, validar_rodape
from commitometro.padroes.referencias import validar_coautoria, validar_referencia

TIPOS_ACEITOS = (
    "feat", "fix", "docs", "style", "refactor", "perf",
    "test", "build", "ci", "chore", "revert",
)


def diagnosticar_cabecalho(linha: str) -> str:
    if not linha.strip():
        return "o cabeçalho está vazio."
    if ": " not in linha:
        if ":" in linha:
            return "falta um espaço depois de ':'."
        return "falta o separador ': ' entre o tipo e a descrição."
    prefixo, descricao = linha.split(": ", 1)
    if prefixo.endswith(" "):
        return "não pode haver espaço antes de ':'."
    prefixo = prefixo.removesuffix("!")
    tipo, abre_escopo, resto = prefixo.partition("(")
    if "!" in tipo:
        return "o '!' deve vir depois do escopo, logo antes de ':'."
    if tipo.lower() in TIPOS_ACEITOS and tipo != tipo.lower():
        return f"o tipo '{tipo}' deve ser minúsculo."
    if tipo not in TIPOS_ACEITOS:
        return f"o tipo '{tipo}' não é aceito; tipos aceitos: {', '.join(TIPOS_ACEITOS)}."
    if abre_escopo:
        if not resto.endswith(")"):
            return "o escopo precisa ser fechado com ')' logo antes de ':'."
        escopo = resto[:-1]
        if not escopo:
            return "o escopo entre parênteses está vazio."
        return f"o escopo '{escopo}' deve ter só letras minúsculas, dígitos e hífens simples."
    if not descricao or descricao.startswith(" "):
        return "a descrição está vazia ou começa com espaço."
    return "o cabeçalho não segue o formato tipo(escopo)!: descrição."


def _paragrafos(mensagem: str) -> list[list[str]]:
    paragrafos: list[list[str]] = []
    atual: list[str] = []
    for linha in mensagem.splitlines():
        if linha.strip():
            atual.append(linha)
        elif atual:
            paragrafos.append(atual)
            atual = []
    if atual:
        paragrafos.append(atual)
    return paragrafos


def bloco_de_rodape(mensagem: str) -> list[Rodape]:
    paragrafos = _paragrafos(mensagem)
    if len(paragrafos) < 2:
        return []
    rodapes = [validar_rodape(linha) for linha in paragrafos[-1]]
    if any(rodape is None for rodape in rodapes):
        return []
    return rodapes


def _issues_do_corpo(linhas: list[str]) -> tuple[str, ...]:
    issues: list[str] = []
    for linha in linhas:
        referencia = validar_referencia(linha)
        if referencia is not None:
            issues.extend(referencia.issues)
    return tuple(dict.fromkeys(issues))


def _coautores_do_corpo(linhas: list[str]) -> tuple[str, ...]:
    emails = (validar_coautoria(linha) for linha in linhas)
    return tuple(dict.fromkeys(coautor.email for coautor in emails if coautor is not None))


def analisar_commit(commit: Commit) -> AnaliseCommit:
    linhas = commit.mensagem.splitlines()
    primeira_linha = linhas[0] if linhas else ""
    corpo = linhas[1:]
    cabecalho = validar_cabecalho(primeira_linha)
    quebra_no_rodape = any(rodape.quebra for rodape in bloco_de_rodape(commit.mensagem))
    return AnaliseCommit(
        commit=commit,
        tipo=cabecalho.tipo if cabecalho else None,
        escopo=cabecalho.escopo if cabecalho else None,
        quebra=(cabecalho is not None and cabecalho.quebra) or quebra_no_rodape,
        valido=cabecalho is not None,
        diagnostico=None if cabecalho else diagnosticar_cabecalho(primeira_linha),
        issues=_issues_do_corpo(corpo),
        coautores=_coautores_do_corpo(corpo),
    )
