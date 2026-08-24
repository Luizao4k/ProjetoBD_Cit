"""
Testes de integração HTTP das rotas de CEMEP.
"""

from __future__ import annotations


def test_criar_cemep_retorna_201(client, escola_id):
    resposta = client.post(
        "/cemeps", json={"escola_id": escola_id, "comentario": "turno da tarde"}
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["escola_id"] == escola_id
    assert corpo["comentario"] == "turno da tarde"


def test_criar_cemep_sem_escola_id_retorna_400(client):
    resposta = client.post("/cemeps", json={"comentario": "sem escola"})

    assert resposta.status_code == 400


def test_criar_segundo_cemep_para_mesma_escola_retorna_409(client, escola_id):
    client.post("/cemeps", json={"escola_id": escola_id})

    resposta = client.post("/cemeps", json={"escola_id": escola_id})

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "EscolaJaPossuiCemepError"


def test_buscar_atualizar_remover_cemep(client, escola_id):
    criado = client.post("/cemeps", json={"escola_id": escola_id}).get_json()

    assert client.get(f"/cemeps/{criado['id']}").status_code == 200

    resposta_put = client.put(f"/cemeps/{criado['id']}", json={"comentario": "novo"})
    assert resposta_put.get_json()["comentario"] == "novo"

    assert client.delete(f"/cemeps/{criado['id']}").status_code == 204
    assert client.get(f"/cemeps/{criado['id']}").status_code == 404
