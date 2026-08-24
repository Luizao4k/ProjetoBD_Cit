"""
Testes de integração HTTP das rotas de Starlink.
"""

from __future__ import annotations


def test_criar_starlink_retorna_201(client, escola_id):
    resposta = client.post(
        "/starlinks", json={"escola_id": escola_id, "designacao": "starlink-01"}
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["designacao"] == "STARLINK-01"  # designacao é Nome: maiusculiza
    assert corpo["escola_id"] == escola_id


def test_criar_starlink_sem_designacao_retorna_400(client, escola_id):
    resposta = client.post("/starlinks", json={"escola_id": escola_id})

    assert resposta.status_code == 400


def test_criar_dois_starlinks_para_mesma_escola_e_permitido(client, escola_id):
    """Diferente de Diretor/CEMEP/Chromebook: Starlink não tem
    restrição de unicidade de escola_id no schema."""
    client.post("/starlinks", json={"escola_id": escola_id, "designacao": "STARLINK-01"})

    resposta = client.post(
        "/starlinks", json={"escola_id": escola_id, "designacao": "STARLINK-02"}
    )

    assert resposta.status_code == 201
    assert len(client.get("/starlinks").get_json()) == 2


def test_buscar_atualizar_remover_starlink(client, escola_id):
    criado = client.post(
        "/starlinks", json={"escola_id": escola_id, "designacao": "STARLINK-01"}
    ).get_json()

    assert client.get(f"/starlinks/{criado['id']}").status_code == 200

    resposta_put = client.put(
        f"/starlinks/{criado['id']}", json={"designacao": "STARLINK-99"}
    )
    assert resposta_put.get_json()["designacao"] == "STARLINK-99"

    assert client.delete(f"/starlinks/{criado['id']}").status_code == 204
    assert client.get(f"/starlinks/{criado['id']}").status_code == 404
