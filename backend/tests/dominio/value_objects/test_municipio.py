import pytest

from domain.value_objects.municipio import Municipio
from shared.exceptions import MunicipioInvalidoError


def test_municipio_valido():
    municipio = Municipio("Belém")

    assert municipio.valor == "Belém"


@pytest.mark.parametrize(
    "valor",
    [
        "",
        "   ",
    ],
)
def test_municipio_invalido(valor):
    with pytest.raises(MunicipioInvalidoError):
        Municipio(valor)