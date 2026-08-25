"""
Registro de rotas de Chromebook.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import chromebook_controller

chromebook_bp = Blueprint("chromebook", __name__, url_prefix="/chromebooks")

chromebook_bp.add_url_rule(
    "", view_func=chromebook_controller.criar_chromebook, methods=["POST"]
)
chromebook_bp.add_url_rule(
    "", view_func=chromebook_controller.listar_chromebooks, methods=["GET"]
)
chromebook_bp.add_url_rule(
    "/<int:chromebook_id>",
    view_func=chromebook_controller.buscar_chromebook,
    methods=["GET"],
)
chromebook_bp.add_url_rule(
    "/<int:chromebook_id>",
    view_func=chromebook_controller.atualizar_chromebook,
    methods=["PUT"],
)
chromebook_bp.add_url_rule(
    "/<int:chromebook_id>",
    view_func=chromebook_controller.remover_chromebook,
    methods=["DELETE"],
)
