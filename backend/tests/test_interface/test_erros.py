"""
Testes de interface.erros.registrar_tratadores_de_erro, isolados de
qualquer controller real — usa uma app Flask descartável com rotas
que só existem para levantar cada tipo de exceção sob teste.

Cobre especificamente os casos que nenhuma rota de DRE consegue
exercitar (DRE não tem restrição de unicidade nem FK): 409 de
duplicidade e 409 dos 7 erros de "possui dependentes".
"""

from __future__ import annotations

import pytest
from flask import Flask

from interface.erros import registrar_tratadores_de_erro
from shared.exceptions import (
    ComentarioInvalidoError,
    DreNaoEncontradaError,
    EscolaNaoPossuiDiretorError,
    EscolaPossuiDiretorError,
    InepJaCadastradoError,
    NomeInvalidoError,
    PersistenciaError,
)


@pytest.fixture
def client():
    app = Flask(__name__)
    registrar_tratadores_de_erro(app)

    @app.route("/erro/dominio")
    def _erro_dominio():
        raise NomeInvalidoError("Nome não pode ser vazio.")

    @app.route("/erro/dominio-comentario")
    def _erro_dominio_comentario():
        raise ComentarioInvalidoError("Comentário muito longo.")

    @app.route("/erro/duplicado")
    def _erro_duplicado():
        raise InepJaCadastradoError("12345678")

    @app.route("/erro/nao-encontrado")
    def _erro_nao_encontrado():
        raise DreNaoEncontradaError(999)

    @app.route("/erro/relacao-ausente")
    def _erro_relacao_ausente():
        raise EscolaNaoPossuiDiretorError(1)

    @app.route("/erro/conflito-integridade")
    def _erro_conflito_integridade():
        raise EscolaPossuiDiretorError(1)

    @app.route("/erro/infraestrutura")
    def _erro_infraestrutura():
        raise PersistenciaError("Falha ao conectar no banco.")

    return app.test_client()


def test_erro_de_dominio_vira_400(client):
    resposta = client.get("/erro/dominio")
    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "NomeInvalidoError"


def test_outro_erro_de_dominio_tambem_vira_400(client):
    """Prova que o handler é por classe-base DomainError, não por
    cada Value Object individualmente registrado."""
    resposta = client.get("/erro/dominio-comentario")
    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "ComentarioInvalidoError"


def test_registro_duplicado_vira_409(client):
    resposta = client.get("/erro/duplicado")
    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "InepJaCadastradoError"


def test_registro_nao_encontrado_vira_404(client):
    resposta = client.get("/erro/nao-encontrado")
    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "DreNaoEncontradaError"


def test_relacao_nao_encontrada_vira_404(client):
    resposta = client.get("/erro/relacao-ausente")
    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "EscolaNaoPossuiDiretorError"


def test_conflito_de_integridade_referencial_vira_409_nao_500(client):
    """O caso não óbvio: EscolaPossuiDiretorError herda de
    PersistenciaError (InfrastructureError), mas semanticamente é o
    cliente tentando remover algo com dependentes -- 409, não 500."""
    resposta = client.get("/erro/conflito-integridade")
    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "EscolaPossuiDiretorError"


def test_erro_de_infraestrutura_generico_vira_500(client):
    resposta = client.get("/erro/infraestrutura")
    assert resposta.status_code == 500
    assert resposta.get_json()["erro"] == "PersistenciaError"
