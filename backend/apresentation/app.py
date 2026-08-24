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

from typing import cast

from flask import Flask, g, request
from flask.json.provider import DefaultJSONProvider

from infrastructure.container.container import Container
from interface.documentacao import documentacao_bp
from interface.erros import registrar_tratadores_de_erro
from interface.routes.dre_routes import dre_bp
from interface.routes.escola_routes import escola_bp
from interface.routes.diretor_routes import diretor_bp
from interface.routes.cemep_routes import cemep_bp
from interface.routes.chromebook_routes import chromebook_bp
from interface.routes.starlink_routes import starlink_bp
from interface.routes.responsavel_routes import responsavel_bp
from interface.routes.turma_cemep_routes import turma_cemep_bp


def criar_app(caminho_banco: str = "escolas.db") -> Flask:
    app = Flask(__name__)
    # app.json é tipado como a base abstrata JSONProvider (extensível
    # por design), mas em tempo de execução é sempre DefaultJSONProvider
    # a menos que alguém troque explicitamente — o cast só informa isso
    # ao mypy, não muda nada em runtime.
    cast(DefaultJSONProvider, app.json).ensure_ascii = False  # nomes/municípios em português, sem \uXXXX

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

    return app
