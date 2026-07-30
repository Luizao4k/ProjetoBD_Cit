import pytest

from time import sleep

from domain.entities import TurmaCemep
from domain.value_objects import Nome
from shared.types import ResponsavelId, TurmaCemepId

@pytest.fixture
def turma():
    return TurmaCemep(
        id=TurmaCemepId(1),
        nome_turma=Nome("Turma A"),
        responsavel_id=ResponsavelId(3),
    )

def test_alterar_nome(turma):
    nome = Nome("Turma B")

    turma.alterar_nome(nome)

    assert turma.nome_turma == nome


