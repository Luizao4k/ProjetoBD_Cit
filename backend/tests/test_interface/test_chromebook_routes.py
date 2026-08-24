"""
Testes de integração HTTP das rotas de Chromebook.
"""

from __future__ import annotations


def test_criar_chromebook_retorna_201(client, escola_id):
    resposta = client.post(
        "/chromebooks", json={"escola_id": escola_id, "kit_aluno": 30, "kit_professor": 2}
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["kit_aluno"] == 30
    assert corpo["kit_professor"] == 2


def test_criar_chromebook_sem_escola_id_retorna_400(client):
    resposta = client.post("/chromebooks", json={"kit_aluno": 30})

    assert resposta.status_code == 400


def test_criar_chromebook_com_kit_negativo_retorna_400(client, escola_id):
    resposta = client.post(
        "/chromebooks", json={"escola_id": escola_id, "kit_aluno": -5}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "QuantidadeInvalidaError"


def test_criar_segundo_chromebook_para_mesma_escola_retorna_409(client, escola_id):
    client.post("/chromebooks", json={"escola_id": escola_id})

    resposta = client.post("/chromebooks", json={"escola_id": escola_id})

    assert resposta.status_code == 409


def test_buscar_atualizar_remover_chromebook(client, escola_id):
    criado = client.post("/chromebooks", json={"escola_id": escola_id}).get_json()

    assert client.get(f"/chromebooks/{criado['id']}").status_code == 200

    resposta_put = client.put(f"/chromebooks/{criado['id']}", json={"kit_aluno": 40})
    assert resposta_put.get_json()["kit_aluno"] == 40

    assert client.delete(f"/chromebooks/{criado['id']}").status_code == 204
    assert client.get(f"/chromebooks/{criado['id']}").status_code == 404
