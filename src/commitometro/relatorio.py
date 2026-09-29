from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from commitometro.modelos import RelatorioAuditoria


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
