import pytest

from domain.entities import Chromebook
from domain.value_objects import Quantidade
from shared.types import ChromebooksId, EscolaId


@pytest.fixture
def chromebook():
    return Chromebook(
        id=ChromebooksId(1),
        escola_id=EscolaId(5),
        kit_aluno=Quantidade(10),
        kit_professor=Quantidade(2),
    )


def test_alterar_kit_aluno(chromebook):
    quantidade = Quantidade(20)

    chromebook.alterar_kit_aluno(quantidade)

    assert chromebook.kit_aluno == quantidade


def test_alterar_kit_professor(chromebook):
    quantidade = Quantidade(5)

    chromebook.alterar_kit_professor(quantidade)

    assert chromebook.kit_professor == quantidade
