import pytest

from commitometro.erros import EntradaInvalidaError
from commitometro.leitores.arquivo import ler_historico, ler_linhas

CAMINHO_HISTORICO = "dados/exemplos/historico_exemplo.log"
CAMINHO_TAGS = "dados/exemplos/tags_exemplo.txt"
CAMINHO_BRANCHES = "dados/exemplos/branches_exemplo.txt"


def test_le_historico_de_exemplo() -> None:
    commits = ler_historico(CAMINHO_HISTORICO)
    assert len(commits) == 25
    assert all(not commit.merge for commit in commits)
    primeiro = commits[0]
    assert primeiro.autor_nome == "Ana Souza"
    assert primeiro.autor_email == "ana.souza@example.com"
    assert primeiro.mensagem == "feat(auth): adiciona login com e-mail e senha"


def test_le_mensagem_com_corpo_multilinhas() -> None:
    commits = ler_historico(CAMINHO_HISTORICO)
    com_corpo = next(c for c in commits if "Closes #18" in c.mensagem)
    assert "\n\n" in com_corpo.mensagem
    assert com_corpo.mensagem.splitlines()[0] == "feat(pagamento): adiciona integração com gateway de cartão"


def test_historico_inexistente_leva_a_erro_amigavel() -> None:
    with pytest.raises(EntradaInvalidaError, match="não existe"):
        ler_historico("dados/exemplos/nao_existe.log")


def test_historico_vazio_leva_a_erro_amigavel(tmp_path) -> None:
    caminho = tmp_path / "vazio.log"
    caminho.write_text("", encoding="utf-8")
    with pytest.raises(EntradaInvalidaError, match="vazio"):
        ler_historico(caminho)


def test_registro_malformado_informa_o_numero(tmp_path) -> None:
    caminho = tmp_path / "malformado.log"
    caminho.write_text("hash\x1fnome\x1femail\x1e", encoding="utf-8")
    with pytest.raises(EntradaInvalidaError, match="registro 1"):
        ler_historico(caminho)


def test_le_tags_de_exemplo() -> None:
    tags = ler_linhas(CAMINHO_TAGS)
    assert "v1.0.0" in tags
    assert len(tags) == 6


def test_le_branches_de_exemplo() -> None:
    branches = ler_linhas(CAMINHO_BRANCHES)
    assert "main" in branches
    assert len(branches) == 8


def test_linhas_inexistente_leva_a_erro_amigavel() -> None:
    with pytest.raises(EntradaInvalidaError, match="não existe"):
        ler_linhas("dados/exemplos/nao_existe.txt")
