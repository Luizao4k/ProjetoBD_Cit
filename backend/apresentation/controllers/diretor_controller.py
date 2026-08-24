"""
Handlers HTTP de Diretor.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.diretor import AtualizarDiretorInput, CriarDiretorInput
from interface.serializacao import dto_para_dict

_CAMPOS_OBRIGATORIOS = ("nome", "escola_id")


def criar_diretor():
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

    dados = CriarDiretorInput(
        escola_id=corpo["escola_id"],
        nome=corpo["nome"],
        telefone=corpo.get("telefone"),
        email=corpo.get("email"),
    )
    saida = g.container.criar_diretor().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_diretores():
    saida = g.container.listar_diretores().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_diretor(diretor_id: int):
    saida = g.container.buscar_diretor_por_id().executar(diretor_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_diretor(diretor_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarDiretorInput(
        id=diretor_id,
        nome=corpo.get("nome"),
        telefone=corpo.get("telefone"),
        email=corpo.get("email"),
    )
    saida = g.container.atualizar_diretor().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_diretor(diretor_id: int):
    g.container.remover_diretor().executar(diretor_id)
    return "", 204
