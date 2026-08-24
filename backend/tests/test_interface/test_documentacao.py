"""
Testes de interface.documentacao — as rotas /openapi.yaml e /docs.
"""

from __future__ import annotations

import yaml


def test_openapi_yaml_retorna_200_e_e_yaml_valido(client):
    resposta = client.get("/openapi.yaml")

    assert resposta.status_code == 200
    assert "yaml" in resposta.content_type

    spec = yaml.safe_load(resposta.data)
    assert spec["openapi"] == "3.0.3"
    assert "/dres" in spec["paths"]


def test_openapi_yaml_descreve_as_8_entidades(client):
    spec = yaml.safe_load(client.get("/openapi.yaml").data)

    caminhos_esperados = [
        "/dres", "/escolas", "/diretores", "/cemeps",
        "/chromebooks", "/starlinks", "/responsaveis", "/turmas-cemep",
    ]
    for caminho in caminhos_esperados:
        assert caminho in spec["paths"], f"{caminho} não está no spec"
        assert f"{caminho}/{{id}}" in spec["paths"], f"{caminho}/{{id}} não está no spec"


def test_docs_retorna_200_html(client):
    resposta = client.get("/docs")

    assert resposta.status_code == 200
    assert "text/html" in resposta.content_type
    assert b"swagger-ui" in resposta.data.lower() or b"SwaggerUIBundle" in resposta.data


def test_rota_de_documentacao_nao_abre_container(client, monkeypatch):
    """/docs e /openapi.yaml não deveriam tocar no banco -- prova
    isso fazendo Container explodir se for chamado, e confirmando que
    a rota funciona mesmo assim."""
    import interface.app as modulo_app

    def _container_que_nao_deveria_ser_chamado(*args, **kwargs):
        raise AssertionError("Container não deveria ser criado para /docs")

    monkeypatch.setattr(modulo_app, "Container", _container_que_nao_deveria_ser_chamado)

    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.yaml").status_code == 200
