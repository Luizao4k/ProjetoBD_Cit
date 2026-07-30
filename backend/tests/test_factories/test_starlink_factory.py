from domain.entities import Starlink
from domain.value_objects import Nome
from shared.types import EscolaId, StarlinkId

from tests.factories.starlink_factory import StarlinkFactory


def test_deve_criar_starlink_valida():
    starlink = StarlinkFactory.criar()

    assert isinstance(starlink, Starlink)

    assert starlink.id == StarlinkId(1)
    assert starlink.designacao == Nome("STARLINK ESCOLA")
    assert starlink.escola_id == EscolaId(1)


def test_deve_permitir_sobrescrever_campos():
    starlink = StarlinkFactory.criar(
        id=15,
        designacao="STARLINK BELÉM",
        escola_id=8,
    )

    assert starlink.id == StarlinkId(15)
    assert starlink.designacao == Nome("STARLINK BELÉM")
    assert starlink.escola_id == EscolaId(8)


def test_deve_permitir_id_none():
    starlink = StarlinkFactory.criar(id=None)

    assert starlink.id is None
