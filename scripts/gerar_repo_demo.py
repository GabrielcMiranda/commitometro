from __future__ import annotations

import os
import shutil
import stat
from pathlib import Path

import git

CAMINHO_DEMO = Path(__file__).resolve().parent.parent / "dados" / "repo_demo"

ANA = git.Actor("Ana Souza", "ana.souza@example.com")
JOAO = git.Actor("João Pedro Lima", "joao.lima@example.com")
BIA = git.Actor("Beatriz Nogueira", "beatriz.nogueira@example.com")

COMMITS = [
    (ANA, "2026-08-01 09:00:00 -0300", "feat(auth): adiciona login com e-mail e senha"),
    (JOAO, "2026-08-01 14:00:00 -0300", "fix(carrinho): corrige cálculo do frete\n\nCloses #3"),
    (BIA, "2026-08-02 10:00:00 -0300", "docs: adiciona instruções de instalação no README"),
    (ANA, "2026-08-02 15:00:00 -0300", "Adiciona botão de finalizar compra"),
    (JOAO, "2026-08-03 09:30:00 -0300", "feat(pagamento): adiciona integração com gateway de cartão\n\nCloses #7"),
    (BIA, "2026-08-03 14:20:00 -0300", "test(carrinho): cobre cálculo de frete"),
    (ANA, "2026-08-04 11:00:00 -0300", "feat(pagamento)!: remove suporte a boleto\n\nBREAKING CHANGE: o método 'boleto' não é mais aceito.\n\nCloses #9"),
    (JOAO, "2026-08-04 16:40:00 -0300", "fix(auth) : corrige expiração do token de sessão"),
    (BIA, "2026-08-05 10:10:00 -0300", "feat(notificacoes): adiciona e-mail de confirmação de pedido\n\nCo-authored-by: Ana Souza <ana.souza@example.com>"),
    (ANA, "2026-08-05 15:35:00 -0300", "refactor(catalogo): extrai filtro de categoria"),
    (JOAO, "2026-08-06 09:05:00 -0300", "feat(carrinho): adiciona cupom de desconto\n\nCloses #12\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"),
    (BIA, "2026-08-06 13:50:00 -0300", "chore(deps): atualiza dependências de desenvolvimento"),
]

TAGS_VALIDAS = ["v0.1.0", "v0.2.0-beta.1"]
TAG_INVALIDA = "versao-final"

BRANCHES_VALIDAS = ["feature/checkout-pix", "release/1.1.0", "docs/atualiza-readme"]
BRANCHES_INVALIDAS = ["nova-feature", "Feature/Login"]


def _remover_somente_leitura(funcao, caminho, excecao) -> None:
    os.chmod(caminho, stat.S_IWRITE)
    funcao(caminho)


def _commitar(repositorio: git.Repo, indice: int, autor: git.Actor, data: str, mensagem: str) -> None:
    nome_arquivo = f"arquivo_{indice:02d}.txt"
    caminho_arquivo = Path(repositorio.working_tree_dir) / nome_arquivo
    caminho_arquivo.write_text(mensagem, encoding="utf-8")
    repositorio.index.add([nome_arquivo])
    repositorio.index.commit(
        mensagem,
        author=autor,
        committer=autor,
        author_date=data,
        commit_date=data,
    )


def gerar() -> Path:
    if CAMINHO_DEMO.exists():
        shutil.rmtree(CAMINHO_DEMO, onexc=_remover_somente_leitura)
    CAMINHO_DEMO.mkdir(parents=True)

    repositorio = git.Repo.init(CAMINHO_DEMO, initial_branch="main")
    for indice, (autor, data, mensagem) in enumerate(COMMITS, start=1):
        _commitar(repositorio, indice, autor, data, mensagem)
        if indice == 4:
            repositorio.create_tag(TAGS_VALIDAS[0])
        if indice == 9:
            repositorio.create_tag(TAGS_VALIDAS[1])

    repositorio.create_tag(TAG_INVALIDA)

    for nome in BRANCHES_VALIDAS + BRANCHES_INVALIDAS:
        repositorio.create_head(nome)

    return CAMINHO_DEMO


if __name__ == "__main__":
    caminho = gerar()
    print(f"Repositório de demonstração criado em {caminho}")
