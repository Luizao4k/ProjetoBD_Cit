"""
Registro de rotas de Escola.
"""

from __future__ import annotations

from flask import Blueprint

from interface.controllers import escola_controller

escola_bp = Blueprint("escola", __name__, url_prefix="/escolas")

escola_bp.add_url_rule("", view_func=escola_controller.criar_escola, methods=["POST"])
escola_bp.add_url_rule("", view_func=escola_controller.listar_escolas, methods=["GET"])
escola_bp.add_url_rule(
    "/<int:escola_id>", view_func=escola_controller.buscar_escola, methods=["GET"]
)
escola_bp.add_url_rule(
    "/<int:escola_id>", view_func=escola_controller.atualizar_escola, methods=["PUT"]
)
escola_bp.add_url_rule(
    "/<int:escola_id>", view_func=escola_controller.remover_escola, methods=["DELETE"]
)
