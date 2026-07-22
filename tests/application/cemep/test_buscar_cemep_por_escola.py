import pytest

from application.use_cases.cemep import BuscarCemepPorEscolaUseCase
from application.use_cases.cemep.dtos import CemepOutput
from shared.exceptions import EscolaNaoPossuiCemepError, PersistenciaInconsistenteError
from tests.factories import CemepFactory

def test_deve_retornar_cemep_por_escola(
    cemep_repository,
    cemep,
):
    cemep_repository.buscar_por_escola.return_value = cemep

    use_case = BuscarCemepPorEscolaUseCase(cemep_repository)

    resultado = use_case.executar(1)

    assert isinstance(resultado, CemepOutput)

    assert resultado.id == cemep.id
    assert resultado.escola_id == cemep.escola_id
    assert resultado.comentario == cemep.comentario

def test_deve_lancar_escola_sem_cemep(
    cemep_repository,
):
    cemep_repository.buscar_por_escola.return_value = None

    use_case = BuscarCemepPorEscolaUseCase(cemep_repository)

    with pytest.raises(EscolaNaoPossuiCemepError):
        use_case.executar(1)

def test_deve_lancar_erro_quando_repositorio_retornar_cemep_id(
    cemep_repository,
):
    cemep = CemepFactory.criar(id=None)

    cemep_repository.buscar_por_escola.return_value = cemep

    use_case = BuscarCemepPorEscolaUseCase(cemep_repository)

    with pytest.raises(PersistenciaInconsistenteError):
        use_case.executar(1)
