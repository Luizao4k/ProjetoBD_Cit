import pytest

from domain.value_objects.comentario import Comentario
from shared.exceptions import ComentarioInvalidoError


def test_comentario_valido():
    comentario = Comentario("Muito bom")

    assert comentario.valor == "Muito bom"


@pytest.mark.parametrize(
    "valor",
    [
        "",
        "   ",
    ],
)
def test_comentario_vazio(valor):
    with pytest.raises(ComentarioInvalidoError):
        Comentario(valor)
