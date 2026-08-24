"""
Registro de rotas de Starlink.
"""

from __future__ import annotations

from flask import Blueprint

from interface.controllers import starlink_controller

starlink_bp = Blueprint("starlink", __name__, url_prefix="/starlinks")

starlink_bp.add_url_rule("", view_func=starlink_controller.criar_starlink, methods=["POST"])
starlink_bp.add_url_rule("", view_func=starlink_controller.listar_starlinks, methods=["GET"])
starlink_bp.add_url_rule(
    "/<int:starlink_id>", view_func=starlink_controller.buscar_starlink, methods=["GET"]
)
starlink_bp.add_url_rule(
    "/<int:starlink_id>", view_func=starlink_controller.atualizar_starlink, methods=["PUT"]
)
starlink_bp.add_url_rule(
    "/<int:starlink_id>",
    view_func=starlink_controller.remover_starlink,
    methods=["DELETE"],
)
