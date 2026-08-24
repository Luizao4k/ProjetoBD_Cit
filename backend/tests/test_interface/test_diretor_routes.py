"""
Testes de integração HTTP das rotas de Diretor.
"""

from __future__ import annotations


def test_criar_diretor_retorna_201(client, escola_id):
    resposta = client.post(
        "/diretores", json={"nome": "Fulano", "escola_id": escola_id, "email": "fulano@escola.com"}
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome"] == "FULANO"  # Nome remove acento e maiusculiza
    assert corpo["escola_id"] == escola_id
    assert corpo["email"] == "fulano@escola.com"


def test_criar_diretor_sem_campo_obrigatorio_retorna_400(client, escola_id):
    resposta = client.post("/diretores", json={"escola_id": escola_id})

    assert resposta.status_code == 400


def test_criar_segundo_diretor_para_mesma_escola_retorna_409(client, escola_id):
    client.post("/diretores", json={"nome": "Fulano", "escola_id": escola_id})

    resposta = client.post("/diretores", json={"nome": "Ciclano", "escola_id": escola_id})

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "EscolaJaPossuiDiretorError"


def test_criar_diretor_com_escola_inexistente_retorna_404(client):
    resposta = client.post("/diretores", json={"nome": "Fulano", "escola_id": 9999})

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "EscolaNaoEncontradaError"


def test_buscar_atualizar_remover_diretor(client, escola_id):
    criado = client.post("/diretores", json={"nome": "Fulano", "escola_id": escola_id}).get_json()

    assert client.get(f"/diretores/{criado['id']}").status_code == 200

    resposta_put = client.put(f"/diretores/{criado['id']}", json={"telefone": "91988887777"})
    assert resposta_put.status_code == 200
    assert resposta_put.get_json()["telefone"] == "91988887777"

    assert client.delete(f"/diretores/{criado['id']}").status_code == 204
    assert client.get(f"/diretores/{criado['id']}").status_code == 404
