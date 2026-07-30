"""
Fixtures compartilhadas por toda a suíte de testes.
"""

from unittest.mock import create_autospec

import pytest

from domain.repositories import (
    CemepRepository,
    ChromebookRepository,
    DiretorRepository,
    DreRepository,
    EscolaRepository,
    ResponsavelRepository,
    StarlinkRepository,
    TurmaCemepRepository,
)

from tests.factories import (
    DreFactory,
    EscolaFactory,
    DiretorFactory,
    CemepFactory,
    ChromebookFactory,
    ResponsavelFactory,
    StarlinkFactory,
    TurmaCemepFactory
)


# ======================================================
# Entidades
# ======================================================

@pytest.fixture
def dre():
    return DreFactory.criar()


@pytest.fixture
def escola():
    return EscolaFactory.criar()


@pytest.fixture
def diretor():
    return DiretorFactory.criar()


@pytest.fixture
def cemep():
    return CemepFactory.criar()


@pytest.fixture
def chromebook():
    return ChromebookFactory.criar()


@pytest.fixture
def responsavel():
    return ResponsavelFactory.criar()


@pytest.fixture
def starlink():
    return StarlinkFactory.criar()


@pytest.fixture
def turma_cemep():
    return TurmaCemepFactory.criar()


# ======================================================
# Repositórios
# ======================================================

@pytest.fixture
def dre_repository():
    return create_autospec(DreRepository)


@pytest.fixture
def escola_repository():
    return create_autospec(EscolaRepository)


@pytest.fixture
def diretor_repository():
    return create_autospec(DiretorRepository)


@pytest.fixture
def cemep_repository():
    return create_autospec(CemepRepository)


@pytest.fixture
def chromebook_repository():
    return create_autospec(ChromebookRepository)


@pytest.fixture
def responsavel_repository():
    return create_autospec(ResponsavelRepository)


@pytest.fixture
def starlink_repository():
    return create_autospec(StarlinkRepository)


@pytest.fixture
def turma_cemep_repository():
    return create_autospec(TurmaCemepRepository)
