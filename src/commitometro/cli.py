from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from commitometro.auditoria import auditar as executar_auditoria
from commitometro.erros import EntradaInvalidaError
from commitometro.padroes import REGISTRO
from commitometro.relatorio import para_json, para_markdown, renderizar_tabela

app = typer.Typer(help="Auditor de convenções de commits e versionamento em repositórios Git.")

_FORMATOS = ("tabela", "json", "markdown")


def _validar_formato(formato: str) -> None:
    if formato not in _FORMATOS:
        raise EntradaInvalidaError(
            f"Formato '{formato}' desconhecido; use um de: {', '.join(_FORMATOS)}."
        )


def _escrever_saida(texto: str, saida: Optional[Path]) -> None:
    if saida is None:
        print(texto)
    else:
        saida.write_text(texto, encoding="utf-8")


def _normalizar_id_er(bruto: str) -> str:
    digitos = "".join(caractere for caractere in bruto if caractere.isdigit())
    return f"ER-{digitos.zfill(2)}" if digitos else bruto.upper()


@contextmanager
def _tratar_entrada_invalida():
    try:
        yield
    except EntradaInvalidaError as erro:
        Console(stderr=True).print(f"[bold red]Erro:[/bold red] {escape(str(erro))}")
        raise typer.Exit(code=2) from None


@app.command()
def auditar(
    caminho: Optional[str] = typer.Argument(None, help="Caminho do repositório Git."),
    arquivo: Optional[Path] = typer.Option(None, "--arquivo", help="Histórico exportado."),
    tags: Optional[Path] = typer.Option(None, "--tags", help="Arquivo de tags exportado."),
    branches: Optional[Path] = typer.Option(None, "--branches", help="Arquivo de branches exportado."),
    formato: str = typer.Option("tabela", "--formato", help="tabela, json ou markdown."),
    saida: Optional[Path] = typer.Option(None, "--saida", help="Arquivo onde salvar a saída."),
    incluir_merges: bool = typer.Option(False, "--incluir-merges"),
    falhar_se_invalido: bool = typer.Option(False, "--falhar-se-invalido"),
) -> None:
    with _tratar_entrada_invalida():
        _validar_formato(formato)
        relatorio = executar_auditoria(
            caminho,
            historico=arquivo,
            arquivo_tags=tags,
            arquivo_branches=branches,
            incluir_merges=incluir_merges,
        )
        if formato == "tabela":
            renderizar_tabela(Console(), relatorio)
        elif formato == "json":
            _escrever_saida(para_json(relatorio), saida)
        else:
            _escrever_saida(para_markdown(relatorio), saida)

        if falhar_se_invalido:
            total_invalidos = sum(len(autor.invalidos) for autor in relatorio.por_autor)
            if total_invalidos:
                raise typer.Exit(code=1)


@app.command()
def validar(er: str, cadeia: str) -> None:
    with _tratar_entrada_invalida():
        chave = _normalizar_id_er(er)
        expressao = REGISTRO.get(chave)
        if expressao is None:
            raise EntradaInvalidaError(
                f"ER desconhecida: '{er}'. IDs válidos: {', '.join(sorted(REGISTRO))}."
            )
        console = Console()
        console.print(f"[bold]{expressao.id}[/bold] — {escape(expressao.nome)}")
        console.print(f"ER formal: {escape(expressao.formal)}")
        console.print(f"Padrão no código: {escape(expressao.padrao)}")

        correspondencia = expressao.compilada.fullmatch(cadeia)
        if correspondencia is None:
            console.print(
                f"[red]rejeitada[/red]: '{escape(cadeia)}' não casa com o padrão de {expressao.id}."
            )
            return

        console.print(f"[green]aceita[/green]: '{escape(cadeia)}'")
        if expressao.grupos:
            tabela = Table(title="Grupos extraídos")
            tabela.add_column("Índice")
            tabela.add_column("Descrição")
            tabela.add_column("Valor")
            for indice, descricao in sorted(expressao.grupos.items()):
                tabela.add_row(str(indice), escape(descricao), escape(correspondencia.group(indice) or ""))
            console.print(tabela)


@app.command()
def versao(
    caminho: Optional[str] = typer.Argument(None, help="Caminho do repositório Git."),
    arquivo: Optional[Path] = typer.Option(None, "--arquivo", help="Histórico exportado."),
    tags: Optional[Path] = typer.Option(None, "--tags", help="Arquivo de tags exportado."),
    pre: Optional[str] = typer.Option(None, "--pre", help="Rótulo de pré-lançamento (alpha, beta, rc)."),
) -> None:
    with _tratar_entrada_invalida():
        relatorio = executar_auditoria(caminho, historico=arquivo, arquivo_tags=tags, pre=pre)
        sugestao = relatorio.sugestao_versao
        console = Console()
        console.print(
            f"{escape(sugestao.versao_anterior or '(nenhuma)')} → "
            f"[bold]{escape(sugestao.versao_sugerida)}[/bold]"
        )
        console.print(escape(sugestao.motivo))


@app.command()
def ers(markdown: bool = typer.Option(False, "--markdown")) -> None:
    with _tratar_entrada_invalida():
        console = Console()
        if markdown:
            for chave in sorted(REGISTRO):
                expressao = REGISTRO[chave]
                console.print(f"## {expressao.id} — {expressao.nome}", markup=False)
                console.print(f"- Formal: `{expressao.formal}`", markup=False)
                console.print(f"- Código: `{expressao.padrao}`", markup=False)
                console.print("")
            return

        tabela = Table(title="Expressões regulares registradas")
        tabela.add_column("ID")
        tabela.add_column("Nome")
        tabela.add_column("ER formal")
        for chave in sorted(REGISTRO):
            expressao = REGISTRO[chave]
            tabela.add_row(expressao.id, escape(expressao.nome), escape(expressao.formal))
        console.print(tabela)
