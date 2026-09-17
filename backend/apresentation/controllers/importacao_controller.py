"""
Handler HTTP de Importação em lote.

Conecta o upload feito pelo frontend (multipart/form-data) aos
scripts de importação já existentes em scripts/importar_*.py (Fase
4) — este controller não reimplementa nenhuma regra de importação,
só: recebe o arquivo enviado, salva num diretório temporário (os
scripts leem por caminho de arquivo, não por stream — ver Reader em
infrastructure/importacao/readers/), delega para a função de
importação correspondente ao "tipo" recebido, serializa o
ResultadoImportacao para JSON e limpa o arquivo temporário.

Cada linha inválida do arquivo vira uma entrada em "falhas" na
resposta, não uma exceção — o ImportadorPipeline já captura erro
linha a linha e nunca deixa uma linha ruim derrubar o lote inteiro
(ver infrastructure/importacao/pipeline.py). Só ArquivoInvalidoError
(arquivo sem as colunas obrigatórias, por exemplo) interrompe a
importação inteira; é tratado aqui do mesmo jeito que os scripts de
CLI tratam esse erro, virando um 400 em vez de subir como exceção
não mapeada.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Callable

from flask import current_app, jsonify, request
from werkzeug.utils import secure_filename

from infrastructure.importacao import ArquivoInvalidoError, ResultadoImportacao
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

# Mesmas chaves que o frontend usa em TipoImportacao (ver
# frontend/src/features/importacao/types/importacao.ts) — uma
# entidade nova precisa ser adicionada nos dois lugares.
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

# Mesmas extensões que infrastructure/importacao/readers/factory.py
# sabe escolher automaticamente — qualquer outra seria lida como CSV
# por criar_reader() e provavelmente falharia linha a linha sem que
# o motivo real (formato errado) ficasse claro pro usuário.
_EXTENSOES_PERMITIDAS = {".csv", ".xlsx", ".xlsm"}


def _erro_requisicao(mensagem: str):
    return jsonify({"erro": "RequisicaoInvalidaError", "mensagem": mensagem}), 400


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
        return _erro_requisicao("Campo 'arquivo' é obrigatório.")

    nome_original = secure_filename(arquivo_enviado.filename) or "importacao"
    extensao = Path(nome_original).suffix.lower()

    if extensao not in _EXTENSOES_PERMITIDAS:
        return _erro_requisicao(
            "Formato de arquivo não suportado. Envie um arquivo .csv, .xlsx ou .xlsm."
        )

    caminho_banco = current_app.config["CAMINHO_BANCO"]

    # Diretório temporário próprio (não o diretório do resultado):
    # os scripts, ao encontrar falhas, gravam um "<nome>_falhas.csv"
    # do LADO do arquivo de origem (ver resultado.exportar_falhas_csv
    # em cada scripts/importar_*.py); um diretório descartável evita
    # que esse efeito colateral vaze pro disco do servidor — a API
    # devolve as falhas no JSON da resposta (campo "falhas"), o
    # frontend monta o CSV de download a partir delas.
    with tempfile.TemporaryDirectory(prefix="importacao_") as diretorio_temp:
        caminho_temp = Path(diretorio_temp) / nome_original
        arquivo_enviado.save(str(caminho_temp))

        try:
            resultado = funcao_importar(caminho_temp, caminho_banco)
        except ArquivoInvalidoError as erro:
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
            "falhas": [dto_para_dict(erro) for erro in resultado.erros],
        }

    return jsonify(corpo), 200
