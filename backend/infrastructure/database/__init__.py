"""
Camada de infraestrutura.

Contém as implementações concretas dos contratos definidos em
domain.repositories. A camada de aplicação (use cases) nunca importa
nada daqui diretamente — é o código de composição (main, testes, API)
que decide qual implementação injetar em cada Use Case.
"""
from .sqlite.connection import criar_conexao
from .sqlite.schema import criar_schema
from .sqlite.transacao import transacao

__all__ = [
    "criar_conexao",
    "criar_schema",
    "transacao",
]