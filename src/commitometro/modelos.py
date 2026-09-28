from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Commit:
    hash: str
    autor_nome: str
    autor_email: str
    data: datetime
    mensagem: str
    merge: bool


@dataclass(frozen=True, slots=True)
class AnaliseCommit:
    commit: Commit
    tipo: str | None
    escopo: str | None
    quebra: bool
    valido: bool
    diagnostico: str | None
    issues: tuple[str, ...]
    coautores: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ConformidadeAutor:
    nome: str
    email: str
    total_commits: int
    commits_validos: int
    percentual_conformidade: float
    distribuicao_por_tipo: dict[str, int]
    commits_com_issue: int
    quebras_declaradas: int
    coautorias_recebidas: int
    invalidos: tuple[AnaliseCommit, ...]


@dataclass(frozen=True, slots=True)
class SugestaoVersao:
    versao_anterior: str | None
    versao_sugerida: str
    tipo_incremento: str
    motivo: str


@dataclass(frozen=True, slots=True)
class RelatorioAuditoria:
    por_autor: tuple[ConformidadeAutor, ...]
    branches_validas: tuple[str, ...]
    branches_invalidas: tuple[str, ...]
    tags_validas: tuple[str, ...]
    tags_invalidas: tuple[str, ...]
    sugestao_versao: SugestaoVersao
