import unicodedata
from dataclasses import dataclass

from shared.exceptions import MunicipioInvalidoError

from .. import MUNICIPIOS_VALIDOS


def _normalizar_chave(valor: str) -> str:
    """
    Normaliza o município para comparação.

    Remove diferenças de:
    - maiúsculas/minúsculas;
    - acentuação;
    - espaços nas extremidades.
    """
    valor = valor.strip().upper()

    valor = unicodedata.normalize("NFD", valor)

    return "".join(
        caractere
        for caractere in valor
        if unicodedata.category(caractere) != "Mn"
    )


# Mapa "chave normalizada" -> grafia oficial.
_MUNICIPIOS_POR_CHAVE = {
    _normalizar_chave(municipio): municipio
    for municipio in MUNICIPIOS_VALIDOS
}


@dataclass(frozen=True)
class Municipio:
    """
    Representa um município válido do Pará.

    A comparação é feita de forma case-insensitive e
    independente de acentuação.

    O valor armazenado permanece na grafia oficial
    definida em MUNICIPIOS_VALIDOS.
    """

    valor: str

    def __post_init__(self) -> None:
        valor = self.valor.strip()

        if not valor:
            raise MunicipioInvalidoError(
                "Município não pode ser vazio."
            )

        chave = _normalizar_chave(valor)

        canonico = _MUNICIPIOS_POR_CHAVE.get(chave)

        if canonico is None:
            raise MunicipioInvalidoError(
                f"'{valor}' não é um município válido do Pará."
            )

        object.__setattr__(
            self,
            "valor",
            canonico,
        )
