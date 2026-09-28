from pathlib import Path

import git
import pytest

from commitometro.auditoria import auditar
from commitometro.erros import EntradaInvalidaError


def test_audita_repositorio_ponta_a_ponta(repo_git) -> None:
    relatorio = auditar(repo_git.working_tree_dir)
    assert len(relatorio.por_autor) == 1
    autora = relatorio.por_autor[0]
    assert autora.email == "ana.souza@example.com"
    assert autora.total_commits == 2
    assert autora.commits_validos == 2
    assert relatorio.tags_validas == ("v0.1.0",)
    assert relatorio.tags_invalidas == ()
    assert "feature/nova-tela" in relatorio.branches_validas


def test_sugestao_de_versao_considera_so_commits_depois_da_ultima_tag(repo_git) -> None:
    (Path(repo_git.working_tree_dir) / "novo.txt").write_text("x", encoding="utf-8")
    repo_git.index.add(["novo.txt"])
    autor = git.Actor("Ana Souza", "ana.souza@example.com")
    repo_git.index.commit("feat(app)!: quebra compatibilidade", author=autor, committer=autor)

    relatorio = auditar(repo_git.working_tree_dir)
    assert relatorio.sugestao_versao.versao_anterior == "v0.1.0"
    assert relatorio.sugestao_versao.versao_sugerida == "v1.0.0"
    assert relatorio.sugestao_versao.tipo_incremento == "maior"


def test_audita_a_partir_de_arquivos_exportados() -> None:
    relatorio = auditar(
        historico="dados/exemplos/historico_exemplo.log",
        arquivo_tags="dados/exemplos/tags_exemplo.txt",
        arquivo_branches="dados/exemplos/branches_exemplo.txt",
    )
    assert len(relatorio.por_autor) == 4
    assert relatorio.sugestao_versao.versao_sugerida == "v2.0.0"


def test_sem_repositorio_e_sem_historico_e_invalido() -> None:
    with pytest.raises(EntradaInvalidaError, match="não os dois"):
        auditar()


def test_repositorio_e_historico_juntos_e_invalido() -> None:
    with pytest.raises(EntradaInvalidaError, match="não os dois"):
        auditar("dados/repo_demo", historico="dados/exemplos/historico_exemplo.log")
