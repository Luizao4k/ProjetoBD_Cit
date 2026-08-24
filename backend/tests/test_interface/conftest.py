"""
Fixtures dos testes de interface (API).

Banco em arquivo real dentro de tmp_path, não ":memory:" — cada
requisição abre sua própria conexão (ver interface/app.py), e
":memory:" cria um banco novo e vazio a cada conexão; um teste que
cria numa requisição e lê noutra precisa que os dados persistam de
verdade entre elas.
"""

from __future__ import annotations

import pytest

from interface.app import criar_app


@pytest.fixture
def app(tmp_path):
    return criar_app(str(tmp_path / "teste.db"))


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def dre_id(client):
    """DRE já persistida via a própria API — usada por todo teste que
    precisa de uma DRE existente sem que a criação da DRE seja o foco
    do teste em si."""
    resposta = client.post("/dres", json={"nome": "DRE Base"})
    return resposta.get_json()["id"]


@pytest.fixture
def escola_id(client, dre_id):
    resposta = client.post(
        "/escolas",
        json={
            "inep": "12345678",
            "nome": "Escola Base",
            "tipo": "MUNICIPAL",
            "municipio": "Belém",
            "dre_id": dre_id,
        },
    )
    return resposta.get_json()["id"]


@pytest.fixture
def cemep_id(client, escola_id):
    resposta = client.post("/cemeps", json={"escola_id": escola_id})
    return resposta.get_json()["id"]


@pytest.fixture
def responsavel_id(client, cemep_id):
    resposta = client.post(
        "/responsaveis", json={"cemep_id": cemep_id, "nome": "Responsável Base"}
    )
    return resposta.get_json()["id"]
