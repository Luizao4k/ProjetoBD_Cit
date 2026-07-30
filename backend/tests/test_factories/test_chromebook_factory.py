from domain.entities import Chromebook
from domain.value_objects import Quantidade
from shared.types import ChromebooksId, EscolaId

from tests.factories.chromebook_factory import ChromebookFactory


def test_deve_criar_chromebook_valido():
    chromebook = ChromebookFactory.criar()

    assert isinstance(chromebook, Chromebook)

    assert chromebook.id == ChromebooksId(1)
    assert chromebook.escola_id == EscolaId(1)
    assert chromebook.kit_aluno == Quantidade(30)
    assert chromebook.kit_professor == Quantidade(2)


def test_deve_permitir_sobrescrever_campos():
    chromebook = ChromebookFactory.criar(
        id=10,
        escola_id=5,
        kit_aluno=40,
        kit_professor=5,
    )

    assert chromebook.id == ChromebooksId(10)
    assert chromebook.escola_id == EscolaId(5)
    assert chromebook.kit_aluno == Quantidade(40)
    assert chromebook.kit_professor == Quantidade(5)


def test_deve_permitir_id_none():
    chromebook = ChromebookFactory.criar(id=None)

    assert chromebook.id is None
