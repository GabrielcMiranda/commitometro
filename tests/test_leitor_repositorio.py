from pathlib import Path

import git
import pytest

from commitometro.erros import EntradaInvalidaError
from commitometro.leitores.repositorio import (
    commits_desde,
    ler_branches,
    ler_commits,
    ler_tags,
)


def test_le_commits_do_repositorio(repo_git) -> None:
    commits = ler_commits(repo_git.working_tree_dir)
    assert len(commits) == 2
    assert commits[0].mensagem == "feat: adiciona readme inicial"
    assert commits[1].autor_email == "ana.souza@example.com"
    assert all(not c.merge for c in commits)


def test_le_tags_do_repositorio(repo_git) -> None:
    assert ler_tags(repo_git.working_tree_dir) == ["v0.1.0"]


def test_le_branches_do_repositorio(repo_git) -> None:
    branches = ler_branches(repo_git.working_tree_dir)
    assert "main" in branches
    assert "feature/nova-tela" in branches


def test_commits_desde_a_tag(repo_git) -> None:
    (Path(repo_git.working_tree_dir) / "novo.txt").write_text("x", encoding="utf-8")
    repo_git.index.add(["novo.txt"])
    autor = repo_git.head.commit.author
    repo_git.index.commit("feat: adiciona novo arquivo", author=autor, committer=autor)
    assert len(commits_desde(repo_git.working_tree_dir, "v0.1.0")) == 1


def test_caminho_inexistente_leva_a_erro_amigavel() -> None:
    with pytest.raises(EntradaInvalidaError, match="não existe"):
        ler_commits("caminho/que/nao/existe")


def test_pasta_sem_repositorio_git_leva_a_erro_amigavel(tmp_path) -> None:
    pasta = tmp_path / "so_uma_pasta"
    pasta.mkdir()
    with pytest.raises(EntradaInvalidaError, match="não é um repositório Git"):
        ler_commits(pasta)


def test_repositorio_sem_commits_leva_a_erro_amigavel(tmp_path) -> None:
    pasta = tmp_path / "vazio"
    pasta.mkdir()
    git.Repo.init(pasta)
    with pytest.raises(EntradaInvalidaError, match="não tem nenhum commit"):
        ler_commits(pasta)
