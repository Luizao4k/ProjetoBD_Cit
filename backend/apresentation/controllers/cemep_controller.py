"""
Handlers HTTP de CEMEP.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.cemep import AtualizarCemepInput, CriarCemepInput
from interface.serializacao import dto_para_dict


def criar_cemep():
    corpo = request.get_json(silent=True) or {}

    if "escola_id" not in corpo:
        return (
            jsonify(
                {
                    "erro": "RequisicaoInvalidaError",
                    "mensagem": "Campo 'escola_id' é obrigatório.",
                }
            ),
            400,
        )

    dados = CriarCemepInput(
        escola_id=corpo["escola_id"],
        comentario=corpo.get("comentario"),
    )
    saida = g.container.criar_cemep().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_cemeps():
    saida = g.container.listar_cemeps().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_cemep(cemep_id: int):
    saida = g.container.buscar_cemep_por_id().executar(cemep_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_cemep(cemep_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarCemepInput(id=cemep_id, comentario=corpo.get("comentario"))
    saida = g.container.atualizar_cemep().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_cemep(cemep_id: int):
    g.container.remover_cemep().executar(cemep_id)
    return "", 204
