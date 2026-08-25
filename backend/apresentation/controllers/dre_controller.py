"""
Handlers HTTP de DRE.

Cada função aqui só: lê a requisição, monta o DTO, chama o caso de
uso já existente via g.container, serializa a saída. Nenhuma
validação de negócio mora aqui — isso é dos Value Objects dentro do
Use Case; qualquer exceção deles sobe até o tratador global
(interface/erros.py), sem try/except neste arquivo.
"""

from __future__ import annotations

from typing import Any, cast
from flask import g, jsonify, request

from backend.application.use_cases.dre import AtualizarDreInput, CriarDreInput
from backend.apresentation.serializacao import dto_para_dict


def criar_dre():
    """
    Cria uma nova DRE.

    Lê os dados da requisição HTTP, monta o DTO de entrada e executa
    o caso de uso responsável pela criação da DRE.

    Returns:
        tuple: Resposta HTTP contendo a DRE criada e o status 201.
    """
    corpo_json = request.get_json(silent=True)

    if not isinstance(corpo_json, dict):
        return (
            jsonify(
                {
                    "erro": "RequisicaoInvalidaError",
                    "mensagem": "O corpo da requisição deve ser um objeto JSON.",
                }
            ),
            400,
        )

    corpo: dict[str, Any] = cast(dict[str, Any], corpo_json)

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

    dados = CriarDreInput(
        nome=corpo["nome"],
        telefone=corpo.get("telefone"),
    )

    saida = g.container.criar_dre().executar(dados)

    return jsonify(dto_para_dict(saida)), 201

def listar_dres():
    """
    Lista todas as DREs cadastradas.

    Executa o caso de uso responsável pela listagem e serializa
    os DTOs de saída para a resposta HTTP.

    Returns:
        tuple: Resposta HTTP contendo a lista de DREs e o status 200.
    """
    saida = g.container.listar_dres().executar()
    return jsonify([dto_para_dict(item) for item in saida]), 200


def buscar_dre(dre_id: int):
    """
    Busca uma DRE pelo identificador.

    Args:
        dre_id: Identificador da DRE.

    Returns:
        tuple: Resposta HTTP contendo a DRE encontrada e o status 200.
    """
    saida = g.container.buscar_dre_por_id().executar(dre_id)
    return jsonify(dto_para_dict(saida)), 200


def atualizar_dre(dre_id: int):
    """
    Atualiza os dados de uma DRE.

    Lê os dados da requisição HTTP, monta o DTO de entrada e executa
    o caso de uso responsável pela atualização.

    Args:
        dre_id: Identificador da DRE a ser atualizada.

    Returns:
        tuple: Resposta HTTP contendo a DRE atualizada e o status 200.
    """
    corpo_json = request.get_json(silent=True)

    if not isinstance(corpo_json, dict):
        return (
            jsonify(
                {
                    "erro": "RequisicaoInvalidaError",
                    "mensagem": "O corpo da requisição deve ser um objeto JSON.",
                }
            ),
            400,
        )

    corpo: dict[str, Any] = cast(dict[str, Any], corpo_json)

    dados = AtualizarDreInput(
        id=dre_id,
        nome=corpo.get("nome"),
        telefone=corpo.get("telefone"),
    )

    saida = g.container.atualizar_dre().executar(dados)

    return jsonify(dto_para_dict(saida)), 200


def remover_dre(dre_id: int):
    """
    Remove uma DRE pelo identificador.

    Args:
        dre_id: Identificador da DRE a ser removida.

    Returns:
        tuple: Resposta HTTP vazia e o status 204.
    """
    g.container.remover_dre().executar(dre_id)
    return "", 204
