"""
Testes de integração do SqliteEscolaRepository (banco real em memória).

Escola é o caso mais delicado do projeto: `remover` pode ser bloqueado
por 4 tabelas diferentes (Diretor, Cemep, Chromebook, Starlink), e o
SQLite não diz qual delas na mensagem de erro — por isso os testes
cobrem cada bloqueio individualmente.
"""

import pytest

from domain.value_objects import Nome, Endereco
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteDiretorRepository,
    SqliteCemepRepository,
    SqliteChromebookRepository,
    SqliteStarlinkRepository,
)
from shared.exceptions import (
    InepJaCadastradoError,
    DreNaoEncontradaError,
    EscolaPossuiDiretorError,
    EscolaPossuiCemepError,
    EscolaPossuiChromebookError,
    EscolaPossuiStarlinksError,
)
from shared.types import DreId
from tests.factories import (
    DreFactory,
    EscolaFactory,
    DiretorFactory,
    CemepFactory,
    ChromebookFactory,
    StarlinkFactory,
)


@pytest.fixture
def dre_salva(conexao):
    return SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))


def test_salvar_atribui_id_e_persiste(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    escola = EscolaFactory.criar(id=None, dre_id=dre_salva.id)

    salva = repo.salvar(escola)

    assert salva.id is not None
    encontrada = repo.buscar_por_id(salva.id)
    assert encontrada is not None
    assert encontrada.inep == salva.inep
    assert encontrada.dre_id == dre_salva.id


def test_salvar_com_inep_duplicado_levanta_erro(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    repo.salvar(EscolaFactory.criar(id=None, inep="15000001", dre_id=dre_salva.id))

    with pytest.raises(InepJaCadastradoError):
        repo.salvar(EscolaFactory.criar(id=None, inep="15000001", dre_id=dre_salva.id))


def test_salvar_com_dre_inexistente_levanta_erro(conexao):
    repo = SqliteEscolaRepository(conexao)

    with pytest.raises(DreNaoEncontradaError):
        repo.salvar(EscolaFactory.criar(id=None, dre_id=DreId(999999)))


def test_buscar_por_nome(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    repo.salvar(EscolaFactory.criar(id=None, nome="escola alfa", dre_id=dre_salva.id))

    encontradas = repo.buscar_por_nome(Nome("escola alfa"))

    assert len(encontradas) == 1


def test_buscar_por_inep(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    salva = repo.salvar(EscolaFactory.criar(id=None, inep="15000002", dre_id=dre_salva.id))

    encontrada = repo.buscar_por_inep(salva.inep)

    assert encontrada is not None
    assert encontrada.id == salva.id


def test_buscar_por_municipio(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    repo.salvar(EscolaFactory.criar(id=None, municipio="Marabá", dre_id=dre_salva.id))
    repo.salvar(EscolaFactory.criar(id=None, inep="15000003", municipio="Marabá", dre_id=dre_salva.id))

    encontradas = repo.buscar_por_municipio("Marabá")

    assert len(encontradas) == 2


def test_buscar_por_dre(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    repo.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))

    encontradas = repo.buscar_por_dre(dre_salva.id)

    assert len(encontradas) == 1


def test_atualizar_persiste_nome_e_endereco_mas_nao_toca_em_campos_imutaveis(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    salva = repo.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))
    inep_original = salva.inep

    salva.nome = Nome("ESCOLA RENOMEADA")
    salva.endereco = Endereco("Rua Nova, 100")
    repo.atualizar(salva)

    relida = repo.buscar_por_id(salva.id)
    assert relida.nome.valor == "ESCOLA RENOMEADA"
    assert relida.endereco.valor == "Rua Nova, 100"
    assert relida.inep == inep_original


def test_remover_sem_dependencias(conexao, dre_salva):
    repo = SqliteEscolaRepository(conexao)
    salva = repo.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))

    repo.remover(salva.id)

    assert repo.buscar_por_id(salva.id) is None


def test_remover_bloqueado_por_diretor(conexao, dre_salva):
    repo_escola = SqliteEscolaRepository(conexao)
    escola = repo_escola.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))
    SqliteDiretorRepository(conexao).salvar(DiretorFactory.criar(id=None, escola_id=escola.id))

    with pytest.raises(EscolaPossuiDiretorError):
        repo_escola.remover(escola.id)


def test_remover_bloqueado_por_cemep(conexao, dre_salva):
    repo_escola = SqliteEscolaRepository(conexao)
    escola = repo_escola.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))
    SqliteCemepRepository(conexao).salvar(CemepFactory.criar(id=None, escola_id=escola.id))

    with pytest.raises(EscolaPossuiCemepError):
        repo_escola.remover(escola.id)


def test_remover_bloqueado_por_chromebook(conexao, dre_salva):
    repo_escola = SqliteEscolaRepository(conexao)
    escola = repo_escola.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))
    SqliteChromebookRepository(conexao).salvar(ChromebookFactory.criar(id=None, escola_id=escola.id))

    with pytest.raises(EscolaPossuiChromebookError):
        repo_escola.remover(escola.id)


def test_remover_bloqueado_por_starlink(conexao, dre_salva):
    repo_escola = SqliteEscolaRepository(conexao)
    escola = repo_escola.salvar(EscolaFactory.criar(id=None, dre_id=dre_salva.id))
    SqliteStarlinkRepository(conexao).salvar(StarlinkFactory.criar(id=None, escola_id=escola.id))

    with pytest.raises(EscolaPossuiStarlinksError):
        repo_escola.remover(escola.id)
