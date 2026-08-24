"""
Handlers HTTP de Responsável.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.responsavel import (
    AtualizarResponsavelInput,
    CriarResponsavelInput,
)
from interface.serializacao import dto_para_dict

_CAMPOS_OBRIGATORIOS = ("cemep_id", "nome")


def criar_responsavel():
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

    dados = CriarResponsavelInput(cemep_id=corpo["cemep_id"], nome=corpo["nome"])
    saida = g.container.criar_responsavel().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_responsaveis():
    saida = g.container.listar_responsaveis().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_responsavel(responsavel_id: int):
    saida = g.container.buscar_responsavel_por_id().executar(responsavel_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_responsavel(responsavel_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarResponsavelInput(id=responsavel_id, nome=corpo.get("nome"))
    saida = g.container.atualizar_responsavel().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_responsavel(responsavel_id: int):
    g.container.remover_responsavel().executar(responsavel_id)
    return "", 204
