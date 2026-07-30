"""
Implementação de persistência em SQLite (stdlib puro, sem dependências
externas — consistente com o resto do projeto).

Uso típico (ex: num main.py de composição):

    from infrastructure.sqlite import criar_conexao, criar_schema, SqliteEscolaRepository
    from application.use_cases.escola import CriarEscolaUseCase

    repo = SqliteEscolaRepository(conexao)
    caso_de_uso = CriarEscolaUseCase(repo)
"""

from .sqlite_cemep_repository import SqliteCemepRepository
from .sqlite_chromebook_repository import SqliteChromebookRepository
from .sqlite_diretor_repository import SqliteDiretorRepository
from .sqlite_dre_repository import SqliteDreRepository
from .sqlite_escola_repository import SqliteEscolaRepository
from .sqlite_responsavel_repository import SqliteResponsavelRepository
from .sqlite_starlink_repository import SqliteStarlinkRepository
from .sqlite_turma_cemep_repository import SqliteTurmaCemepRepository

__all__ = [
    "SqliteCemepRepository",
    "SqliteChromebookRepository",
    "SqliteDiretorRepository",
    "SqliteDreRepository",
    "SqliteEscolaRepository",
    "SqliteResponsavelRepository",
    "SqliteStarlinkRepository",
    "SqliteTurmaCemepRepository",
]
