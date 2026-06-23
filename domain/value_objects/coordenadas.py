"""
responsável por garantir que latitude e longitude sempre sejam válidas.
"""

from dataclasses import dataclass

from shared.exceptions import ValorInvalidoError


@dataclass(frozen=True)
class Coordenadas:
    """
    Value Object que representa uma localização geográfica.

    Regras:
    - Latitude entre -90 e 90.
    - Longitude entre -180 e 180.
    - É imutável.
    """
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitude <= 90.0:
            raise ValorInvalidoError(
                f"Latitude inválida: {self.latitude}"
            )

        if not -180.0 <= self.longitude <= 180.0:
            raise ValorInvalidoError(
                f"Longitude inválida: {self.longitude}"
            )

    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"
