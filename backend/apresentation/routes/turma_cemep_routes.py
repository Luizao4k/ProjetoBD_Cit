"""
Registro de rotas de Turma CEMEP.
"""

from __future__ import annotations

from flask import Blueprint

from apresentation.controllers import turma_cemep_controller

turma_cemep_bp = Blueprint("turma_cemep", __name__, url_prefix="/turmas-cemep")

turma_cemep_bp.add_url_rule(
    "", view_func=turma_cemep_controller.criar_turma_cemep, methods=["POST"]
)
turma_cemep_bp.add_url_rule(
    "", view_func=turma_cemep_controller.listar_turmas_cemep, methods=["GET"]
)
turma_cemep_bp.add_url_rule(
    "/<int:turma_id>",
    view_func=turma_cemep_controller.buscar_turma_cemep,
    methods=["GET"],
)
turma_cemep_bp.add_url_rule(
    "/<int:turma_id>",
    view_func=turma_cemep_controller.atualizar_turma_cemep,
    methods=["PUT"],
)
turma_cemep_bp.add_url_rule(
    "/<int:turma_id>",
    view_func=turma_cemep_controller.remover_turma_cemep,
    methods=["DELETE"],
)
