"""
Handlers HTTP de Starlink.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.starlink import AtualizarStarlinkInput, CriarStarlinkInput
from interface.serializacao import dto_para_dict

_CAMPOS_OBRIGATORIOS = ("escola_id", "designacao")


def criar_starlink():
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

    dados = CriarStarlinkInput(escola_id=corpo["escola_id"], designacao=corpo["designacao"])
    saida = g.container.criar_starlink().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_starlinks():
    saida = g.container.listar_starlinks().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_starlink(starlink_id: int):
    saida = g.container.buscar_starlink_por_id().executar(starlink_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_starlink(starlink_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarStarlinkInput(id=starlink_id, designacao=corpo.get("designacao"))
    saida = g.container.atualizar_starlink().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_starlink(starlink_id: int):
    g.container.remover_starlink().executar(starlink_id)
    return "", 204
