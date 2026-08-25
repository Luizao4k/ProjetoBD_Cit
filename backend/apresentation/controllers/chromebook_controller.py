"""
Handlers HTTP de Chromebook.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.chromebook import (
    AtualizarChromebookInput,
    CriarChromebookInput,
)
from apresentation.serializacao import dto_para_dict


def criar_chromebook():
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

    dados = CriarChromebookInput(
        escola_id=corpo["escola_id"],
        kit_aluno=corpo.get("kit_aluno"),
        kit_professor=corpo.get("kit_professor"),
    )
    saida = g.container.criar_chromebook().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_chromebooks():
    saida = g.container.listar_chromebooks().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_chromebook(chromebook_id: int):
    saida = g.container.buscar_chromebook_por_id().executar(chromebook_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_chromebook(chromebook_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarChromebookInput(
        id=chromebook_id,
        kit_aluno=corpo.get("kit_aluno"),
        kit_professor=corpo.get("kit_professor"),
    )
    saida = g.container.atualizar_chromebook().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_chromebook(chromebook_id: int):
    g.container.remover_chromebook().executar(chromebook_id)
    return "", 204
