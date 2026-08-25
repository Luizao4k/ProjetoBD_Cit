"""
Registro de rotas de Responsável.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import responsavel_controller

responsavel_bp = Blueprint("responsavel", __name__, url_prefix="/responsaveis")

responsavel_bp.add_url_rule(
    "", view_func=responsavel_controller.criar_responsavel, methods=["POST"]
)
responsavel_bp.add_url_rule(
    "", view_func=responsavel_controller.listar_responsaveis, methods=["GET"]
)
responsavel_bp.add_url_rule(
    "/<int:responsavel_id>",
    view_func=responsavel_controller.buscar_responsavel,
    methods=["GET"],
)
responsavel_bp.add_url_rule(
    "/<int:responsavel_id>",
    view_func=responsavel_controller.atualizar_responsavel,
    methods=["PUT"],
)
responsavel_bp.add_url_rule(
    "/<int:responsavel_id>",
    view_func=responsavel_controller.remover_responsavel,
    methods=["DELETE"],
)
