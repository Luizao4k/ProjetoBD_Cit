"""
Exceções de domínio
"""

class DomainError(Exception):
    """Erro base de domínio — nunca expõe detalhes de infraestrutura."""


class EntidadeNaoEncontradaError(DomainError):
    """Erro de Entidade não encontrada"""
    def __init__(self, entidade: str, id_: int) -> None:
        super().__init__(f"{entidade} com id={id_} não encontrada.")


class RegraDeNegocioVioladaError(DomainError):
    """Violação de uma regra de negócio explícita do domínio."""


class ValorInvalidoError(DomainError):
    """Value object recebeu um valor que não satisfaz suas invariantes."""
