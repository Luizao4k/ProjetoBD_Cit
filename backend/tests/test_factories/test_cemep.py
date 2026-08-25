from domain.entities import Cemep
from shared.types import CemepId, EscolaId

from tests.factories.cemep_factory import CemepFactory


def test_deve_criar_cemep_valido():
    cemep = CemepFactory.criar()

    assert isinstance(cemep, Cemep)

    assert cemep.id == CemepId(1)
    assert cemep.escola_id == EscolaId(1)
    assert cemep.comentario.valor == "Comentário teste"


def test_deve_permitir_sobrescrever_campos():
    cemep = CemepFactory.criar(
        id=25,
        escola_id=99,
        comentario="Novo comentário",
    )

    assert cemep.id == CemepId(25)
    assert cemep.escola_id == EscolaId(99)
    assert cemep.comentario.valor == "Novo comentário"


def test_deve_criar_cemep_sem_id():
    cemep = CemepFactory.criar(id=None)

    assert cemep.id is None
