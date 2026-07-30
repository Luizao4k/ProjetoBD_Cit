from domain.entities import TurmaCemep
from domain.value_objects import Nome
from shared.types import ResponsavelId, TurmaCemepId

from tests.factories.turma_cemep_factory import TurmaCemepFactory


def test_deve_criar_turma_valida():
    turma = TurmaCemepFactory.criar()

    assert isinstance(turma, TurmaCemep)

    assert turma.id == TurmaCemepId(1)
    assert turma.nome_turma == Nome("TURMA A")
    assert turma.responsavel_id == ResponsavelId(1)


def test_deve_permitir_sobrescrever_campos():
    turma = TurmaCemepFactory.criar(
        id=9,
        nome_turma="TURMA B",
        responsavel_id=7,
    )

    assert turma.id == TurmaCemepId(9)
    assert turma.nome_turma == Nome("TURMA B")
    assert turma.responsavel_id == ResponsavelId(7)


def test_deve_permitir_id_none():
    turma = TurmaCemepFactory.criar(id=None)

    assert turma.id is None
