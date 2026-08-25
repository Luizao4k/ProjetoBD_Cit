"""
Registro de rotas de Diretor.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import diretor_controller

diretor_bp = Blueprint("diretor", __name__, url_prefix="/diretores")

diretor_bp.add_url_rule("", view_func=diretor_controller.criar_diretor, methods=["POST"])
diretor_bp.add_url_rule("", view_func=diretor_controller.listar_diretores, methods=["GET"])
diretor_bp.add_url_rule(
    "/<int:diretor_id>", view_func=diretor_controller.buscar_diretor, methods=["GET"]
)
diretor_bp.add_url_rule(
    "/<int:diretor_id>", view_func=diretor_controller.atualizar_diretor, methods=["PUT"]
)
diretor_bp.add_url_rule(
    "/<int:diretor_id>", view_func=diretor_controller.remover_diretor, methods=["DELETE"]
)
