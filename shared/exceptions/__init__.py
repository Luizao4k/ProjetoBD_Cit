"""
Exceções de domínio
"""
from __future__ import annotations

from typing import Final

class DomainError(Exception):
    """Erro base de domínio — nunca expõe detalhes de infraestrutura."""


class EntidadeNaoEncontradaError(DomainError):
    """Erro de Entidade não encontrada"""
    def __init__(self, entidade: str, id_: int) -> None:
        super().__init__(f"{entidade} com id={id_} não encontrada.")
        self.entidade: Final[str] = entidade
        self.id_: Final[int | str] = id_

class EntidadeDuplicadaError(DomainError):
    """Erro de Entidade duplicada"""
    def __init__(self, entidade: str, campo: str, valor: str) -> None:
        super().__init__(f"{entidade} com {campo} '{valor}' já existe.")
        self.entidade: Final[str] = entidade
        self.campo:  Final[str] = campo
        self.valor:  Final[str] = valor

class CampoInvalidoError(DomainError):
    """Erro de campo inválido"""
    def __init__(self, campo: str, motivo: str) -> None:
        super().__init__(f"Campo '{campo}' inválido: {motivo}.")
        self.campo:  Final[str] = campo
        self.motivo: Final[str] = motivo

class NomeInvalidoError(DomainError):
    """Nome inválido para o sistema"""

class TelefoneInvalidoError(DomainError):
    """Telefone inválido para o sistema"""

class EmailInvalidoError(DomainError):
    """Email inválido para o sistema"""

class EnderecoInvalidoError(DomainError):
    """Endereco inválido para o sistema"""

class MunicipioInvalidoError(DomainError):
    """Municipio inválido para o sistema"""

class RegraDeNegocioVioladaError(DomainError):
    """Violação de uma regra de negócio explícita do domínio."""


class ValorInvalidoError(DomainError):
    """Value object recebeu um valor que não satisfaz suas invariantes."""
