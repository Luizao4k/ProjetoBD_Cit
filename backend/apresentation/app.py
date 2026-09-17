"""
App factory da API REST (Fase 5).

Gerenciamento de conexão: um Container novo por requisição HTTP,
guardado em flask.g e fechado no teardown — não um Container global
compartilhado entre requisições concorrentes.

Por quê: a conexão aberta por Container usa check_same_thread=False
(infrastructure/database/sqlite/connection.py), o que permite usá-la
fora da thread em que foi criada — mas não torna o objeto seguro para
uso *concorrente* por várias threads ao mesmo tempo. Um Container
global único, reaproveitado entre requisições paralelas (o padrão que
os scripts de CLI usam, onde é seguro por rodarem sequencialmente),
correria esse risco aqui. Por isso: uma conexão por requisição.
"""

from __future__ import annotations
from flask_cors import CORS
from typing import cast

from flask import Flask, g, request
from flask.json.provider import DefaultJSONProvider

from infrastructure.container.container import Container
from apresentation.documentacao import documentacao_bp
from apresentation.erros import registrar_tratadores_de_erro
from apresentation.routes.dre_routes import dre_bp
from apresentation.routes.escola_routes import escola_bp
from apresentation.routes.diretor_routes import diretor_bp
from apresentation.routes.cemep_routes import cemep_bp
from apresentation.routes.chromebook_routes import chromebook_bp
from apresentation.routes.starlink_routes import starlink_bp
from apresentation.routes.responsavel_routes import responsavel_bp
from apresentation.routes.turma_cemep_routes import turma_cemep_bp
from apresentation.routes.importacao_routes import importacao_bp


def criar_app(caminho_banco: str = "escolas.db") -> Flask:
    app = Flask(__name__)
    CORS(
        app,
        origins=["http://localhost:5173"],
    )
    # app.json é tipado como a base abstrata JSONProvider (extensível
    # por design), mas em tempo de execução é sempre DefaultJSONProvider
    # a menos que alguém troque explicitamente — o cast só informa isso
    # ao mypy, não muda nada em runtime.
    cast(DefaultJSONProvider, app.json).ensure_ascii = False  # nomes/municípios em português, sem \uXXXX

    # Os scripts de importação (scripts/importar_*.py, Fase 4) abrem
    # sua PRÓPRIA conexão via criar_conexao(caminho_banco) — não usam
    # g.container (ver Container.finalizar). O controller de
    # importação precisa do mesmo caminho_banco recebido aqui pra
    # gravar no mesmo arquivo SQLite que o resto da API usa; guardado
    # em app.config (lido via current_app dentro do controller) em vez
    # de virar parâmetro de view function, que o Flask não permite.
    app.config["CAMINHO_BANCO"] = caminho_banco

    @app.before_request
    def _abrir_container() -> None:
        if request.blueprint == "documentacao":
            # /docs e /openapi.yaml são estáticos — não tocam no
            # banco, não precisam de um Container por requisição.
            return
        g.container = Container(caminho_banco)

    @app.teardown_appcontext
    def _fechar_container(excecao: BaseException | None) -> None:
        """
        Roda ao final de toda requisição, mesmo quando um
        errorhandler já transformou a exceção numa resposta JSON
        limpa — Flask passa a exceção original aqui de qualquer
        forma, exatamente para que este tipo de limpeza (rollback)
        aconteça mesmo quando a resposta ao cliente não é um 500.
        """
        container: Container | None = g.pop("container", None)
        if container is not None:
            container.finalizar(sucesso=excecao is None)

    registrar_tratadores_de_erro(app)

    app.register_blueprint(documentacao_bp)
    app.register_blueprint(dre_bp)
    app.register_blueprint(escola_bp)
    app.register_blueprint(diretor_bp)
    app.register_blueprint(cemep_bp)
    app.register_blueprint(chromebook_bp)
    app.register_blueprint(starlink_bp)
    app.register_blueprint(responsavel_bp)
    app.register_blueprint(turma_cemep_bp)
    app.register_blueprint(importacao_bp)

    return app
