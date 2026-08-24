"""
Handlers HTTP de Escola.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.escola import AtualizarEscolaInput, CriarEscolaInput
from interface.serializacao import dto_para_dict

_CAMPOS_OBRIGATORIOS = ("inep", "nome", "tipo", "municipio", "dre_id")


def criar_escola():
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

    dados = CriarEscolaInput(
        inep=corpo["inep"],
        nome=corpo["nome"],
        tipo=corpo["tipo"],
        municipio=corpo["municipio"],
        dre_id=corpo["dre_id"],
        endereco=corpo.get("endereco"),
    )
    saida = g.container.criar_escola().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_escolas():
    saida = g.container.listar_escolas().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_escola(escola_id: int):
    saida = g.container.buscar_escola_por_id().executar(escola_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_escola(escola_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarEscolaInput(
        id=escola_id,
        nome=corpo.get("nome"),
        endereco=corpo.get("endereco"),
    )
    saida = g.container.atualizar_escola().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_escola(escola_id: int):
    g.container.remover_escola().executar(escola_id)
    return "", 204
