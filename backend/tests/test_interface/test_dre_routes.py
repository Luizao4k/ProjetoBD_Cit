"""
Testes de integração HTTP das rotas de DRE — via Flask test client,
sem servidor real.
"""

from __future__ import annotations


def test_criar_dre_retorna_201_com_nome_normalizado(client):
    resposta = client.post("/dres", json={"nome": "dre belém", "telefone": "91999998888"})

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome"] == "DRE BELEM"  # Nome remove acento e maiusculiza
    assert corpo["telefone"] == "91999998888"
    assert corpo["id"] == 1
    assert "criado_em" in corpo and "atualizado_em" in corpo


def test_criar_dre_sem_nome_retorna_400(client):
    resposta = client.post("/dres", json={"telefone": "91999998888"})

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "RequisicaoInvalidaError"


def test_criar_dre_com_nome_vazio_retorna_400_erro_de_dominio(client):
    resposta = client.post("/dres", json={"nome": "   "})

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "NomeInvalidoError"


def test_listar_dres_vazio_de_inicio(client):
    resposta = client.get("/dres")

    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_criar_e_depois_listar_persiste_entre_requisicoes(client):
    """Prova de que o Container por requisição funciona de verdade:
    dado criado numa chamada POST aparece numa chamada GET seguinte,
    mesmo cada uma abrindo sua própria conexão."""
    client.post("/dres", json={"nome": "DRE BELEM"})
    client.post("/dres", json={"nome": "DRE MARABA"})

    resposta = client.get("/dres")

    assert resposta.status_code == 200
    nomes = {item["nome"] for item in resposta.get_json()}
    assert nomes == {"DRE BELEM", "DRE MARABA"}


def test_buscar_dre_por_id_retorna_200(client):
    criado = client.post("/dres", json={"nome": "DRE BELEM"}).get_json()

    resposta = client.get(f"/dres/{criado['id']}")

    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "DRE BELEM"


def test_buscar_dre_inexistente_retorna_404(client):
    resposta = client.get("/dres/9999")

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "DreNaoEncontradaError"


def test_atualizar_dre_retorna_200_com_dados_atualizados(client):
    criado = client.post("/dres", json={"nome": "DRE BELEM"}).get_json()

    resposta = client.put(f"/dres/{criado['id']}", json={"telefone": "91988887777"})

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["nome"] == "DRE BELEM"  # não enviado, permanece
    assert corpo["telefone"] == "91988887777"


def test_atualizar_dre_inexistente_retorna_404(client):
    resposta = client.put("/dres/9999", json={"nome": "Novo Nome"})

    assert resposta.status_code == 404


def test_remover_dre_retorna_204_e_some_da_listagem(client):
    criado = client.post("/dres", json={"nome": "DRE BELEM"}).get_json()

    resposta = client.delete(f"/dres/{criado['id']}")
    assert resposta.status_code == 204
    assert resposta.data == b""

    assert client.get("/dres").get_json() == []


def test_remover_dre_inexistente_retorna_404(client):
    resposta = client.delete("/dres/9999")

    assert resposta.status_code == 404


def test_rota_inexistente_retorna_404_em_json_nao_html(client):
    resposta = client.get("/rota/que/nao/existe")

    assert resposta.status_code == 404
    assert resposta.content_type == "application/json"


def test_metodo_nao_permitido_retorna_405_em_json(client):
    resposta = client.patch("/dres")

    assert resposta.status_code == 405
    assert resposta.content_type == "application/json"
