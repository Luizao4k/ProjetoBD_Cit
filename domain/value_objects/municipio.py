"""
Regras de negócio para municipio.
"""

from dataclasses import dataclass


from shared.exceptions import MunicipioInvalidoError

@dataclass(frozen=True)
class Municipio:
    """Verificação simples"""
    valor: str

    def __post_init__(self):
        valor = self.valor.strip()

        if not valor:
            raise MunicipioInvalidoError("Município não pode ser vazio.")

        object.__setattr__(self, "valor", valor)
