import pytest

from time import sleep

from domain.entities import Starlink
from domain.value_objects import Nome
from shared.types import StarlinkId, EscolaId

@pytest.fixture
def starlink():
    return Starlink(
        id=StarlinkId(1),
        designacao=Nome("SL-01"),
        escola_id=EscolaId(10),
    )


def test_alterar_designacao(starlink):
    designacao = Nome("SL-02")

    starlink.alterar_designacao(designacao)

    assert starlink.designacao == designacao

