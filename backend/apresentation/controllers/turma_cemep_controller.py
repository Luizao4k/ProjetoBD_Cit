"""
Handlers HTTP de Turma CEMEP.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.turma_cemep import (
    AtualizarTurmaCemepInput,
    CriarTurmaCemepInput,
)
from apresentation.serializacao import dto_para_dict

_CAMPOS_OBRIGATORIOS = ("responsavel_id", "nome_turma")


def criar_turma_cemep():
    corpo = request.get_json(silent=True) or {}

    faltando = [c for c in _CAMPOS_OBRIGATORIOS if c not in corpo]
    if faltando:
        return (
            jsonify(
                {
                    "erro": "RequisicaoInvalidaError",
                    "mensagem": f"Campo(s) obrigatório(s) ausente(s): {', '.join(faltando)}.",
                }
            ),
            400,
        )

    dados = CriarTurmaCemepInput(
        responsavel_id=corpo["responsavel_id"], nome_turma=corpo["nome_turma"]
    )
    saida = g.container.criar_turma_cemep().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_turmas_cemep():
    saida = g.container.listar_turmas_cemep().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_turma_cemep(turma_id: int):
    saida = g.container.buscar_turma_cemep_por_id().executar(turma_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_turma_cemep(turma_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarTurmaCemepInput(id=turma_id, nome_turma=corpo.get("nome_turma"))
    saida = g.container.atualizar_turma_cemep().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_turma_cemep(turma_id: int):
    g.container.remover_turma_cemep().executar(turma_id)
    return "", 204
