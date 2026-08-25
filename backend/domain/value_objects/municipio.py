"""
Regras de negócio para município.
"""

from dataclasses import dataclass

from shared.exceptions import MunicipioInvalidoError
from .. import MUNICIPIOS_VALIDOS

# Mapa "chave em minúsculo" -> grafia oficial, construído uma única vez
# no import do módulo (não a cada instanciação de Municipio).
_MUNICIPIOS_POR_CHAVE = {municipio.lower(): municipio for municipio in MUNICIPIOS_VALIDOS}


@dataclass(frozen=True)
class Municipio:
    """
    Regras:
    - Deve corresponder a um dos 144 municípios do Pará (MUNICIPIOS_VALIDOS).
    - A comparação é case-insensitive; o valor final é sempre normalizado
      para a grafia oficial da lista, então "marabá", "MARABÁ" e "Marabá"
      resultam todos no mesmo Municipio(valor="Marabá").
    """
    valor: str

    def __post_init__(self):
        valor = self.valor.strip()

        if not valor:
            raise MunicipioInvalidoError("Município não pode ser vazio.")

        canonico = _MUNICIPIOS_POR_CHAVE.get(valor.lower())

        if canonico is None:
            raise MunicipioInvalidoError(
                f"'{valor}' não é um município válido do Pará."
            )

        object.__setattr__(self, "valor", canonico)
