import git
import pytest


@pytest.fixture
def repo_git(tmp_path):
    caminho = tmp_path / "repo"
    caminho.mkdir()
    repositorio = git.Repo.init(caminho, initial_branch="main")
    autor = git.Actor("Ana Souza", "ana.souza@example.com")

    (caminho / "README.md").write_text("commitômetro\n", encoding="utf-8")
    repositorio.index.add(["README.md"])
    repositorio.index.commit(
        "feat: adiciona readme inicial",
        author=autor,
        committer=autor,
        author_date="2026-08-01 09:00:00 -0300",
        commit_date="2026-08-01 09:00:00 -0300",
    )

    (caminho / "app.py").write_text("print('ola')\n", encoding="utf-8")
    repositorio.index.add(["app.py"])
    repositorio.index.commit(
        "feat(app): adiciona ponto de entrada\n\nCloses #1",
        author=autor,
        committer=autor,
        author_date="2026-08-02 10:00:00 -0300",
        commit_date="2026-08-02 10:00:00 -0300",
    )

    repositorio.create_tag("v0.1.0")
    repositorio.create_head("feature/nova-tela")

    return repositorio
