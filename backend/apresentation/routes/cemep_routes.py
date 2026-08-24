"""
Registro de rotas de CEMEP.
"""

from __future__ import annotations

from flask import Blueprint

from interface.controllers import cemep_controller

cemep_bp = Blueprint("cemep", __name__, url_prefix="/cemeps")

cemep_bp.add_url_rule("", view_func=cemep_controller.criar_cemep, methods=["POST"])
cemep_bp.add_url_rule("", view_func=cemep_controller.listar_cemeps, methods=["GET"])
cemep_bp.add_url_rule(
    "/<int:cemep_id>", view_func=cemep_controller.buscar_cemep, methods=["GET"]
)
cemep_bp.add_url_rule(
    "/<int:cemep_id>", view_func=cemep_controller.atualizar_cemep, methods=["PUT"]
)
cemep_bp.add_url_rule(
    "/<int:cemep_id>", view_func=cemep_controller.remover_cemep, methods=["DELETE"]
)
