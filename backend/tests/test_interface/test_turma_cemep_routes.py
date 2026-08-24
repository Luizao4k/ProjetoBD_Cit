"""
Testes de integração HTTP das rotas de Turma CEMEP.
"""

from __future__ import annotations


def test_criar_turma_retorna_201(client, responsavel_id):
    resposta = client.post(
        "/turmas-cemep",
        json={"responsavel_id": responsavel_id, "nome_turma": "turma a"},
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome_turma"] == "TURMA A"  # nome_turma é Nome: maiusculiza
    assert corpo["responsavel_id"] == responsavel_id


def test_criar_turma_sem_campo_obrigatorio_retorna_400(client, responsavel_id):
    resposta = client.post("/turmas-cemep", json={"responsavel_id": responsavel_id})

    assert resposta.status_code == 400


def test_criar_turma_com_responsavel_inexistente_retorna_404(client):
    resposta = client.post(
        "/turmas-cemep", json={"responsavel_id": 9999, "nome_turma": "Turma A"}
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "ResponsavelNaoEncontradoError"


def test_criar_duas_turmas_para_mesmo_responsavel_e_permitido(client, responsavel_id):
    client.post(
        "/turmas-cemep", json={"responsavel_id": responsavel_id, "nome_turma": "Turma A"}
    )

    resposta = client.post(
        "/turmas-cemep", json={"responsavel_id": responsavel_id, "nome_turma": "Turma B"}
    )

    assert resposta.status_code == 201
    assert len(client.get("/turmas-cemep").get_json()) == 2


def test_buscar_atualizar_remover_turma(client, responsavel_id):
    criada = client.post(
        "/turmas-cemep", json={"responsavel_id": responsavel_id, "nome_turma": "Turma A"}
    ).get_json()

    assert client.get(f"/turmas-cemep/{criada['id']}").status_code == 200

    resposta_put = client.put(
        f"/turmas-cemep/{criada['id']}", json={"nome_turma": "Turma Renomeada"}
    )
    assert resposta_put.get_json()["nome_turma"] == "TURMA RENOMEADA"

    assert client.delete(f"/turmas-cemep/{criada['id']}").status_code == 204
    assert client.get(f"/turmas-cemep/{criada['id']}").status_code == 404
