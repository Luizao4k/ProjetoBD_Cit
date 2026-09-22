"""
Registro de rotas de Importação — separado do controller de
propósito, mesmo padrão dos demais recursos (ver dre_routes.py):

este arquivo só sabe "qual URL/verbo HTTP aponta pra qual função";
a lógica do handler mora em controllers/importacao_controller.py.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import importacao_controller


importacao_bp = Blueprint(
    "importacao",
    __name__,
    url_prefix="/importacao",
)


importacao_bp.add_url_rule(
    "",
    view_func=importacao_controller.importar_dados,
    methods=["POST"],
)

importacao_bp.add_url_rule(
    "/formulario",
    view_func=importacao_controller.importar_formulario,
    methods=["POST"],
)
