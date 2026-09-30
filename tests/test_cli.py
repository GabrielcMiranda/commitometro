from typer.testing import CliRunner

from commitometro.cli import app

runner = CliRunner()

CAMINHO_HISTORICO = "dados/exemplos/historico_exemplo.log"
CAMINHO_TAGS = "dados/exemplos/tags_exemplo.txt"
CAMINHO_BRANCHES = "dados/exemplos/branches_exemplo.txt"


def _invocar(*args: str):
    return runner.invoke(app, list(args))


def test_auditar_tabela_com_arquivo() -> None:
    resultado = _invocar("auditar", "--arquivo", CAMINHO_HISTORICO)
    assert resultado.exit_code == 0
    assert "Resumo da auditoria" in resultado.output


def test_auditar_json_para_arquivo(tmp_path) -> None:
    saida = tmp_path / "saida.json"
    resultado = _invocar(
        "auditar", "--arquivo", CAMINHO_HISTORICO, "--formato", "json", "--saida", str(saida)
    )
    assert resultado.exit_code == 0
    assert saida.exists()
    assert "por_autor" in saida.read_text(encoding="utf-8")


def test_auditar_markdown_com_tags_e_branches() -> None:
    resultado = _invocar(
        "auditar",
        "--arquivo",
        CAMINHO_HISTORICO,
        "--tags",
        CAMINHO_TAGS,
        "--branches",
        CAMINHO_BRANCHES,
        "--formato",
        "markdown",
    )
    assert resultado.exit_code == 0
    assert "# Relatório de auditoria" in resultado.output


def test_auditar_falhar_se_invalido_sai_com_erro() -> None:
    resultado = _invocar("auditar", "--arquivo", CAMINHO_HISTORICO, "--falhar-se-invalido")
    assert resultado.exit_code == 1


def test_auditar_caminho_inexistente() -> None:
    resultado = _invocar("auditar", "caminho/que/nao/existe")
    assert resultado.exit_code == 2
    assert "Erro" in resultado.output
    assert "Traceback" not in resultado.output


def test_auditar_repositorio_e_arquivo_juntos(repo_git) -> None:
    resultado = _invocar("auditar", repo_git.working_tree_dir, "--arquivo", CAMINHO_HISTORICO)
    assert resultado.exit_code == 2


def test_auditar_sem_nenhuma_origem() -> None:
    resultado = _invocar("auditar")
    assert resultado.exit_code == 2


def test_auditar_formato_desconhecido() -> None:
    resultado = _invocar("auditar", "--arquivo", CAMINHO_HISTORICO, "--formato", "xml")
    assert resultado.exit_code == 2


def test_validar_cadeia_aceita() -> None:
    resultado = _invocar("validar", "er03", "v1.2.3")
    assert resultado.exit_code == 0
    assert "aceita" in resultado.output


def test_validar_cadeia_rejeitada() -> None:
    resultado = _invocar("validar", "er01", "Feat: errado")
    assert resultado.exit_code == 0
    assert "rejeitada" in resultado.output


def test_validar_cadeia_vazia_e_rejeitada_sem_erro() -> None:
    resultado = _invocar("validar", "er01", "")
    assert resultado.exit_code == 0
    assert "rejeitada" in resultado.output


def test_validar_er_desconhecida() -> None:
    resultado = _invocar("validar", "er99", "x")
    assert resultado.exit_code == 2
    assert "ER desconhecida" in resultado.output


def test_versao_com_repositorio(repo_git) -> None:
    resultado = _invocar("versao", repo_git.working_tree_dir)
    assert resultado.exit_code == 0


def test_versao_com_arquivo() -> None:
    resultado = _invocar("versao", "--arquivo", CAMINHO_HISTORICO, "--tags", CAMINHO_TAGS)
    assert resultado.exit_code == 0


def test_ers_tabela() -> None:
    resultado = _invocar("ers")
    assert resultado.exit_code == 0
    assert "ER-01" in resultado.output
    assert "ER-06" in resultado.output


def test_ers_markdown() -> None:
    resultado = _invocar("ers", "--markdown")
    assert resultado.exit_code == 0
    assert "## ER-01" in resultado.output
