from __future__ import annotations

import json

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from commitometro.modelos import AnaliseCommit, Commit, ConformidadeAutor, RelatorioAuditoria


def _cor_percentual(percentual: float) -> str:
    if percentual >= 90:
        return "green"
    if percentual >= 60:
        return "yellow"
    return "red"


def renderizar_tabela(console: Console, relatorio: RelatorioAuditoria) -> None:
    total_commits = sum(autor.total_commits for autor in relatorio.por_autor)
    total_validos = sum(autor.commits_validos for autor in relatorio.por_autor)
    percentual_geral = round(100 * total_validos / total_commits, 1) if total_commits else 0.0
    cor_geral = _cor_percentual(percentual_geral)

    console.print(
        Panel(
            f"[bold]{total_commits}[/bold] commits · [bold]{total_validos}[/bold] válidos · "
            f"[bold {cor_geral}]{percentual_geral}%[/bold {cor_geral}] de conformidade geral",
            title="Resumo da auditoria",
        )
    )

    tabela_autores = Table(title="Conformidade por autor")
    tabela_autores.add_column("Autor")
    tabela_autores.add_column("Commits", justify="right")
    tabela_autores.add_column("Válidos", justify="right")
    tabela_autores.add_column("% conformidade", justify="right")
    tabela_autores.add_column("Coautorias recebidas", justify="right")
    for autor in relatorio.por_autor:
        cor = _cor_percentual(autor.percentual_conformidade)
        tabela_autores.add_row(
            escape(autor.nome),
            str(autor.total_commits),
            str(autor.commits_validos),
            f"[{cor}]{autor.percentual_conformidade}%[/{cor}]",
            str(autor.coautorias_recebidas),
        )
    console.print(tabela_autores)

    tabela_branches = Table(title="Branches")
    tabela_branches.add_column("Nome")
    tabela_branches.add_column("Situação")
    for nome in relatorio.branches_validas:
        tabela_branches.add_row(escape(nome), "[green]válida[/green]")
    for nome in relatorio.branches_invalidas:
        tabela_branches.add_row(escape(nome), "[red]inválida[/red]")
    console.print(tabela_branches)

    tabela_tags = Table(title="Tags")
    tabela_tags.add_column("Nome")
    tabela_tags.add_column("Situação")
    for nome in relatorio.tags_validas:
        tabela_tags.add_row(escape(nome), "[green]válida[/green]")
    for nome in relatorio.tags_invalidas:
        tabela_tags.add_row(escape(nome), "[red]inválida[/red]")
    console.print(tabela_tags)

    sugestao = relatorio.sugestao_versao
    console.print(
        Panel(
            f"{escape(sugestao.versao_anterior or '(nenhuma)')} → "
            f"[bold]{escape(sugestao.versao_sugerida)}[/bold]\n{escape(sugestao.motivo)}",
            title="Sugestão de versão",
        )
    )

    invalidos = [analise for autor in relatorio.por_autor for analise in autor.invalidos]
    if invalidos:
        tabela_invalidos = Table(title="Commits inválidos")
        tabela_invalidos.add_column("Hash")
        tabela_invalidos.add_column("Mensagem")
        tabela_invalidos.add_column("Motivo")
        for analise in invalidos:
            primeira_linha = analise.commit.mensagem.splitlines()[0] if analise.commit.mensagem else ""
            tabela_invalidos.add_row(
                analise.commit.hash[:7], escape(primeira_linha), escape(analise.diagnostico or "")
            )
        console.print(tabela_invalidos)


def _commit_para_dict(commit: Commit) -> dict:
    return {
        "hash": commit.hash,
        "autor_nome": commit.autor_nome,
        "autor_email": commit.autor_email,
        "data": commit.data.isoformat(),
        "mensagem": commit.mensagem,
        "merge": commit.merge,
    }


def _analise_para_dict(analise: AnaliseCommit) -> dict:
    return {
        "commit": _commit_para_dict(analise.commit),
        "tipo": analise.tipo,
        "escopo": analise.escopo,
        "quebra": analise.quebra,
        "valido": analise.valido,
        "diagnostico": analise.diagnostico,
        "issues": list(analise.issues),
        "coautores": list(analise.coautores),
    }


def _autor_para_dict(autor: ConformidadeAutor) -> dict:
    return {
        "nome": autor.nome,
        "email": autor.email,
        "total_commits": autor.total_commits,
        "commits_validos": autor.commits_validos,
        "percentual_conformidade": autor.percentual_conformidade,
        "distribuicao_por_tipo": autor.distribuicao_por_tipo,
        "commits_com_issue": autor.commits_com_issue,
        "quebras_declaradas": autor.quebras_declaradas,
        "coautorias_recebidas": autor.coautorias_recebidas,
        "invalidos": [_analise_para_dict(analise) for analise in autor.invalidos],
    }


def _relatorio_para_dict(relatorio: RelatorioAuditoria) -> dict:
    return {
        "por_autor": [_autor_para_dict(autor) for autor in relatorio.por_autor],
        "branches_validas": list(relatorio.branches_validas),
        "branches_invalidas": list(relatorio.branches_invalidas),
        "tags_validas": list(relatorio.tags_validas),
        "tags_invalidas": list(relatorio.tags_invalidas),
        "sugestao_versao": {
            "versao_anterior": relatorio.sugestao_versao.versao_anterior,
            "versao_sugerida": relatorio.sugestao_versao.versao_sugerida,
            "tipo_incremento": relatorio.sugestao_versao.tipo_incremento,
            "motivo": relatorio.sugestao_versao.motivo,
        },
    }


def para_json(relatorio: RelatorioAuditoria) -> str:
    return json.dumps(_relatorio_para_dict(relatorio), ensure_ascii=False, indent=2)


def para_markdown(relatorio: RelatorioAuditoria) -> str:
    linhas = ["# Relatório de auditoria", "", "## Conformidade por autor", ""]
    linhas.append("| Autor | Commits | Válidos | % conformidade | Coautorias recebidas |")
    linhas.append("|---|---|---|---|---|")
    for autor in relatorio.por_autor:
        linhas.append(
            f"| {autor.nome} | {autor.total_commits} | {autor.commits_validos} | "
            f"{autor.percentual_conformidade}% | {autor.coautorias_recebidas} |"
        )

    linhas += ["", "## Branches", ""]
    linhas += [f"- ✅ `{nome}`" for nome in relatorio.branches_validas]
    linhas += [f"- ❌ `{nome}`" for nome in relatorio.branches_invalidas]

    linhas += ["", "## Tags", ""]
    linhas += [f"- ✅ `{nome}`" for nome in relatorio.tags_validas]
    linhas += [f"- ❌ `{nome}`" for nome in relatorio.tags_invalidas]

    sugestao = relatorio.sugestao_versao
    linhas += [
        "",
        "## Sugestão de versão",
        "",
        f"{sugestao.versao_anterior or '(nenhuma)'} → **{sugestao.versao_sugerida}**",
        "",
        sugestao.motivo,
    ]

    invalidos = [analise for autor in relatorio.por_autor for analise in autor.invalidos]
    if invalidos:
        linhas += ["", "## Commits inválidos", "", "| Hash | Mensagem | Motivo |", "|---|---|---|"]
        for analise in invalidos:
            primeira_linha = analise.commit.mensagem.splitlines()[0] if analise.commit.mensagem else ""
            linhas.append(f"| `{analise.commit.hash[:7]}` | {primeira_linha} | {analise.diagnostico} |")

    return "\n".join(linhas) + "\n"
