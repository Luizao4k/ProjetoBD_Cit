"""
Handler HTTP de Importação em lote.

Conecta o upload feito pelo frontend (multipart/form-data) aos
scripts de importação já existentes em scripts/importar_*.py.

O controller não reimplementa nenhuma regra de importação.
Ele recebe o arquivo, salva em diretório temporário, delega a
importação, serializa o ResultadoImportacao para JSON e limpa
o arquivo temporário.

Cada linha inválida do arquivo vira uma entrada em "falhas" na
resposta. O ImportadorPipeline captura os erros linha a linha.

Somente EntradaImportacaoInvalidaError, como arquivo sem as
colunas obrigatórias, interrompe a importação inteira.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Callable

from flask import current_app, jsonify, request
from werkzeug.utils import secure_filename

from application.use_cases.starlink import CriarStarlinkUseCase

from infrastructure.importacao import (
    EntradaImportacaoInvalidaError,
    ImportadorPipeline,
    ResultadoImportacao,
)

from infrastructure.database import (
    GerenciadorDeTransacaoSqlite,
    criar_conexao,
    criar_schema,
)

from infrastructure.database.sqlite.repositories import (
    SqliteEscolaRepository,
    SqliteStarlinkRepository,
)

from infrastructure.importacao.mappers import StarlinkMapper
from infrastructure.importacao.readers import FormularioReader

from apresentation.serializacao import dto_para_dict

from scripts.importar_dres import importar_dres
from scripts.importar_escolas import importar_escolas
from scripts.importar_diretores import importar_diretores
from scripts.importar_cemeps import importar_cemeps
from scripts.importar_chromebooks import importar_chromebooks
from scripts.importar_starlinks import importar_starlinks
from scripts.importar_responsaveis import importar_responsaveis
from scripts.importar_turmas_cemep import importar_turmas_cemep


FuncaoImportar = Callable[..., ResultadoImportacao]


_FUNCOES_IMPORTACAO: dict[str, FuncaoImportar] = {
    "dre": importar_dres,
    "escolas": importar_escolas,
    "diretores": importar_diretores,
    "cemeps": importar_cemeps,
    "chromebooks": importar_chromebooks,
    "starlinks": importar_starlinks,
    "responsaveis": importar_responsaveis,
    "turmas_cemep": importar_turmas_cemep,
}


_EXTENSOES_PERMITIDAS = {
    ".csv",
    ".xlsx",
    ".xlsm",
}


def _erro_requisicao(mensagem: str):
    return jsonify(
        {
            "erro": "RequisicaoInvalidaError",
            "mensagem": mensagem,
        }
    ), 400


def importar_dados():
    tipo = request.form.get("tipo", "")

    funcao_importar = _FUNCOES_IMPORTACAO.get(tipo)

    if funcao_importar is None:
        return _erro_requisicao(
            f"Tipo de importação '{tipo}' é inválido. "
            f"Valores aceitos: {', '.join(_FUNCOES_IMPORTACAO)}."
        )

    arquivo_enviado = request.files.get("arquivo")

    if arquivo_enviado is None or not arquivo_enviado.filename:
        return _erro_requisicao(
            "Campo 'arquivo' é obrigatório."
        )

    nome_original = (
        secure_filename(arquivo_enviado.filename)
        or "importacao"
    )

    extensao = Path(nome_original).suffix.lower()

    if extensao not in _EXTENSOES_PERMITIDAS:
        return _erro_requisicao(
            "Formato de arquivo não suportado. "
            "Envie um arquivo .csv, .xlsx ou .xlsm."
        )

    caminho_banco = current_app.config["CAMINHO_BANCO"]

    with tempfile.TemporaryDirectory(
        prefix="importacao_"
    ) as diretorio_temp:

        caminho_temp = Path(diretorio_temp) / nome_original

        arquivo_enviado.save(str(caminho_temp))

        try:
            resultado = funcao_importar(
                caminho_temp,
                caminho_banco,
            )

        except EntradaImportacaoInvalidaError as erro:
            return (
                jsonify(
                    {
                        "erro": "ArquivoInvalidoError",
                        "mensagem": "; ".join(erro.problemas),
                    }
                ),
                400,
            )

        corpo = {
            "tipo": tipo,
            "arquivo": arquivo_enviado.filename,
            "total_processado": resultado.total_processado,
            "sucessos": len(resultado.sucessos),
            "erros": len(resultado.erros),
            "taxa_sucesso": resultado.taxa_sucesso,
            "resumo": resultado.resumo(),
            "falhas": [
                dto_para_dict(erro)
                for erro in resultado.erros
            ],
        }

    return jsonify(corpo), 200


def importar_formulario():
    """
    Importa uma entidade enviada diretamente por formulário.

    O formulário utiliza o mesmo ImportadorPipeline utilizado
    pela importação de arquivos.
    """

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return _erro_requisicao(
            "O corpo da requisição deve ser um objeto JSON."
        )

    tipo = dados.get("tipo")

    if tipo != "starlinks":
        return _erro_requisicao(
            f"Tipo de importação '{tipo}' não é suportado "
            "para formulário."
        )

    linha = dados.get("dados")

    if not isinstance(linha, dict):
        return _erro_requisicao(
            "O campo 'dados' deve ser um objeto."
        )

    linha_bruta = {
        str(chave): str(valor)
        for chave, valor in linha.items()
    }

    caminho_banco = current_app.config["CAMINHO_BANCO"]

    conexao = criar_conexao(caminho_banco)

    try:
        criar_schema(conexao)

        repo_escola = SqliteEscolaRepository(conexao)
        repo_starlink = SqliteStarlinkRepository(conexao)

        pipeline = ImportadorPipeline(
            reader=FormularioReader(linha_bruta),
            mapper=StarlinkMapper(repo_escola),
            use_case=CriarStarlinkUseCase(repo_starlink),
            gerenciador_transacao=GerenciadorDeTransacaoSqlite(
                conexao
            ),
        )

        resultado = pipeline.executar()

    finally:
        conexao.close()

    corpo = {
        "tipo": tipo,
        "arquivo": None,
        "total_processado": resultado.total_processado,
        "sucessos": len(resultado.sucessos),
        "erros": len(resultado.erros),
        "taxa_sucesso": resultado.taxa_sucesso,
        "resumo": resultado.resumo(),
        "falhas": [
            dto_para_dict(erro)
            for erro in resultado.erros
        ],
    }

    return jsonify(corpo), 200
