"""
Handlers HTTP de DRE.

Cada função aqui só: lê a requisição, monta o DTO, chama o caso de
uso já existente via g.container, serializa a saída. Nenhuma
validação de negócio mora aqui — isso é dos Value Objects dentro do
Use Case; qualquer exceção deles sobe até o tratador global
(interface/erros.py), sem try/except neste arquivo.
"""

from __future__ import annotations

from flask import g, jsonify, request

from application.use_cases.dre import AtualizarDreInput, CriarDreInput
from interface.serializacao import dto_para_dict


def criar_dre():
    corpo = request.get_json(silent=True) or {}

    if "nome" not in corpo:
        return (
            jsonify(
                {
                    "erro": "RequisicaoInvalidaError",
                    "mensagem": "Campo 'nome' é obrigatório.",
                }
            ),
            400,
        )

    dados = CriarDreInput(nome=corpo["nome"], telefone=corpo.get("telefone"))
    saida = g.container.criar_dre().executar(dados)

    return jsonify(dto_para_dict(saida)), 201


def listar_dres():
    saida = g.container.listar_dres().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_dre(dre_id: int):
    saida = g.container.buscar_dre_por_id().executar(dre_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_dre(dre_id: int):
    corpo = request.get_json(silent=True) or {}

    dados = AtualizarDreInput(
        id=dre_id,
        nome=corpo.get("nome"),
        telefone=corpo.get("telefone"),
    )
    saida = g.container.atualizar_dre().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_dre(dre_id: int):
    g.container.remover_dre().executar(dre_id)
    return "", 204
