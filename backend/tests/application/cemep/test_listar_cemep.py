import pytest

from application.use_cases.cemep import ListarCemepsUseCase
from application.use_cases.cemep.dtos import CemepOutput
from shared.exceptions import PersistenciaInconsistenteError
from tests.factories import CemepFactory

def test_deve_retornar_lista_vazia_quando_nao_existirem_cemeps(
    cemep_repository,
):
    cemep_repository.listar_todas.return_value = []

    use_case = ListarCemepsUseCase(cemep_repository)

    resultado = use_case.executar()

    assert resultado == []

def test_deve_retornar_lista_com_cemeps(
        cemep_repository,
):
    cemeps = [
    CemepFactory.criar(id=1),
    CemepFactory.criar(id=2),
]

    cemep_repository.listar_todas.return_value = cemeps
    use_case = ListarCemepsUseCase(cemep_repository)
    resultado = use_case.executar()

    assert isinstance(resultado, list)
    assert len(resultado) == 2

    assert all(isinstance(item, CemepOutput) for item in resultado)

    assert resultado[0].id == cemeps[0].id
    assert resultado[1].id == cemeps[1].id

def test_deve_lancar_erro_quando_repositorio_retornar_entidade_sem_id(
    cemep_repository,
):
    cemep = CemepFactory.criar(id=None)

    cemep_repository.listar_todas.return_value = [cemep]

    use_case = ListarCemepsUseCase(cemep_repository)

    with pytest.raises(
        PersistenciaInconsistenteError,
        match="sem id",
    ):
        use_case.executar()
