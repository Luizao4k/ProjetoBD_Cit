"""
Registro de rotas de DRE — separado do controller de propósito: este
arquivo só sabe "qual URL/verbo HTTP aponta pra qual função"; a lógica
de cada handler mora em interface/controllers/dre_controller.py.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import dre_controller

dre_bp = Blueprint("dre", __name__, url_prefix="/dres")

dre_bp.add_url_rule("", view_func=dre_controller.criar_dre, methods=["POST"])
dre_bp.add_url_rule("", view_func=dre_controller.listar_dres, methods=["GET"])
dre_bp.add_url_rule(
    "/<int:dre_id>", view_func=dre_controller.buscar_dre, methods=["GET"]
)
dre_bp.add_url_rule(
    "/<int:dre_id>", view_func=dre_controller.atualizar_dre, methods=["PUT"]
)
dre_bp.add_url_rule(
    "/<int:dre_id>", view_func=dre_controller.remover_dre, methods=["DELETE"]
)
