"""
Regras de negócio para endereço de Enderecço
"""

from dataclasses import dataclass

from shared.exceptions import EnderecoInvalidoError

@dataclass(frozen=True)
class Endereco:
    """Verificação simples"""
    valor: str

    def __post_init__(self):
        valor = self.valor.strip()

        if not valor:
            raise EnderecoInvalidoError("Endereço não pode ser vazio.")

        object.__setattr__(self, "valor", valor)
