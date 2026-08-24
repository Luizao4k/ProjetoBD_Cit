"""
Testes de integração HTTP das rotas de Responsável.
"""

from __future__ import annotations


def test_criar_responsavel_retorna_201(client, cemep_id):
    resposta = client.post(
        "/responsaveis", json={"cemep_id": cemep_id, "nome": "responsavel teste"}
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome"] == "RESPONSAVEL TESTE"
    assert corpo["cemep_id"] == cemep_id


def test_criar_responsavel_sem_campo_obrigatorio_retorna_400(client, cemep_id):
    resposta = client.post("/responsaveis", json={"cemep_id": cemep_id})

    assert resposta.status_code == 400


def test_criar_responsavel_com_cemep_inexistente_retorna_404(client):
    resposta = client.post("/responsaveis", json={"cemep_id": 9999, "nome": "Alguém"})

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "CemepNaoEncontradoError"


def test_criar_dois_responsaveis_para_mesmo_cemep_e_permitido(client, cemep_id):
    client.post("/responsaveis", json={"cemep_id": cemep_id, "nome": "Responsável A"})

    resposta = client.post(
        "/responsaveis", json={"cemep_id": cemep_id, "nome": "Responsável B"}
    )

    assert resposta.status_code == 201
    assert len(client.get("/responsaveis").get_json()) == 2


def test_buscar_atualizar_remover_responsavel(client, cemep_id):
    criado = client.post(
        "/responsaveis", json={"cemep_id": cemep_id, "nome": "Responsável A"}
    ).get_json()

    assert client.get(f"/responsaveis/{criado['id']}").status_code == 200

    resposta_put = client.put(
        f"/responsaveis/{criado['id']}", json={"nome": "Nome Novo"}
    )
    assert resposta_put.get_json()["nome"] == "NOME NOVO"

    assert client.delete(f"/responsaveis/{criado['id']}").status_code == 204
    assert client.get(f"/responsaveis/{criado['id']}").status_code == 404
