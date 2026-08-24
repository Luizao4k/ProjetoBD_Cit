"""
Testes de integração HTTP das rotas de Escola.
"""

from __future__ import annotations


def test_criar_escola_retorna_201(client, dre_id):
    resposta = client.post(
        "/escolas",
        json={
            "inep": "12345678",
            "nome": "Escola Teste",
            "tipo": "MUNICIPAL",
            "municipio": "Belém",
            "dre_id": dre_id,
        },
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["inep"] == "12345678"
    assert corpo["tipo"] == "MUNICIPAL"
    assert corpo["dre_id"] == dre_id


def test_criar_escola_com_tipo_invalido_retorna_400(client, dre_id):
    """tipo vem de um Enum puro do stdlib (TipoEscola), não de um
    Value Object com exceção própria -- prova que o ValueError bruto
    ainda assim vira um 400 limpo, não um 500."""
    resposta = client.post(
        "/escolas",
        json={
            "inep": "12345678",
            "nome": "Escola Teste",
            "tipo": "PARTICULAR",
            "municipio": "Belém",
            "dre_id": dre_id,
        },
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "ValueError"


def test_criar_escola_sem_campo_obrigatorio_retorna_400(client, dre_id):
    resposta = client.post(
        "/escolas", json={"nome": "Escola Teste", "dre_id": dre_id}
    )

    assert resposta.status_code == 400
    corpo = resposta.get_json()
    assert corpo["erro"] == "RequisicaoInvalidaError"
    assert "inep" in corpo["mensagem"]
    assert "tipo" in corpo["mensagem"]
    assert "municipio" in corpo["mensagem"]


def test_criar_escola_com_dre_inexistente_retorna_404(client):
    resposta = client.post(
        "/escolas",
        json={
            "inep": "12345678",
            "nome": "Escola Teste",
            "tipo": "MUNICIPAL",
            "municipio": "Belém",
            "dre_id": 9999,
        },
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "DreNaoEncontradaError"


def test_criar_escola_com_inep_duplicado_retorna_409(client, dre_id):
    corpo_escola = {
        "inep": "12345678",
        "nome": "Escola A",
        "tipo": "MUNICIPAL",
        "municipio": "Belém",
        "dre_id": dre_id,
    }
    client.post("/escolas", json=corpo_escola)

    resposta = client.post("/escolas", json={**corpo_escola, "nome": "Escola B"})

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "InepJaCadastradoError"


def test_buscar_escola_por_id(client, escola_id):
    resposta = client.get(f"/escolas/{escola_id}")

    assert resposta.status_code == 200
    assert resposta.get_json()["id"] == escola_id


def test_listar_escolas(client, escola_id):
    resposta = client.get("/escolas")

    assert resposta.status_code == 200
    assert len(resposta.get_json()) == 1


def test_atualizar_escola(client, escola_id):
    resposta = client.put(f"/escolas/{escola_id}", json={"endereco": "Rua Nova, 1"})

    assert resposta.status_code == 200
    assert resposta.get_json()["endereco"] == "Rua Nova, 1"


def test_remover_escola(client, escola_id):
    resposta = client.delete(f"/escolas/{escola_id}")

    assert resposta.status_code == 204
    assert client.get(f"/escolas/{escola_id}").status_code == 404


def test_remover_escola_com_diretor_vinculado_retorna_409(client, escola_id):
    client.post("/diretores", json={"nome": "Diretor Teste", "escola_id": escola_id})

    resposta = client.delete(f"/escolas/{escola_id}")

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "EscolaPossuiDiretorError"
