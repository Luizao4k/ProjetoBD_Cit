"""
Exceções base do domínio.

Todas as exceções específicas do domínio devem herdar de DomainError.
"""
from __future__ import annotations


class DomainError(Exception):
    """Classe base para erros do domínio."""


class ApplicationError(Exception):
    """Classe base para erros de Value Objects."""

class PersistenciaInconsistenteError(RuntimeError):
    """Lançada quando o repositório retorna uma entidade em estado inválido."""
