"""
Importa Escolas em lote a partir de um CSV ou Excel (.xlsx/.xlsm), usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_escolas caminho/para/escolas.csv [caminho/do/banco.db]

O formato é escolhido automaticamente pela extensão do
arquivo (ver importacao.readers.criar_reader).

Colunas esperadas:
    inep, nome, tipo, municipio (obrigatórias)
    endereco (opcional)
    dre_id OU dre_nome (pelo menos uma, para vincular a escola à DRE)

Ordem de importação: rode depois de scripts.importar_dres — este
importador resolve dre_id contra DREs já cadastradas no banco.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import (
    GerenciadorDeTransacaoSqlite,
    criar_conexao,
    criar_schema,
)
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
)
from application.use_cases.escola import CriarEscolaUseCase

from infrastructure.importacao import EntradaImportacaoInvalidaError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import criar_reader
from infrastructure.importacao.mappers import EscolaMapper


def importar_escolas(
    caminho_arquivo: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_dre = SqliteDreRepository(conexao)
    repo_escola = SqliteEscolaRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=criar_reader(
            caminho_arquivo, colunas_obrigatorias=EscolaMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=EscolaMapper(repo_dre),
        use_case=CriarEscolaUseCase(repo_escola),
        gerenciador_transacao=GerenciadorDeTransacaoSqlite(conexao),
    )

    resultado = pipeline.executar()

    if resultado.erros:
        caminho_falhas = Path(caminho_arquivo).with_name(
            f"{Path(caminho_arquivo).stem}_falhas.csv"
        )
        resultado.exportar_falhas_csv(caminho_falhas)
        print(f"Falhas gravadas em: {caminho_falhas}")

    conexao.close()
    return resultado


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.importar_escolas caminho/para/escolas.csv [banco.db]")
        sys.exit(1)

    try:
        importar_escolas(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db")
    except EntradaImportacaoInvalidaError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
