"""
Importa Escolas em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_escolas caminho/para/escolas.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    inep, nome, tipo, municipio (obrigatórias)
    endereco (opcional)
    dre_id OU dre_nome (pelo menos uma, para vincular a escola à DRE)

Ordem de importação: rode depois de scripts.importar_dres — este
importador resolve dre_id contra DREs já cadastradas no banco.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
)
from application.use_cases.escola import CriarEscolaUseCase

from infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import CsvReader
from infrastructure.importacao.mappers import EscolaMapper


def importar_escolas(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_dre = SqliteDreRepository(conexao)
    repo_escola = SqliteEscolaRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=EscolaMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=EscolaMapper(repo_dre),
        use_case=CriarEscolaUseCase(repo_escola),
    )

    resultado = pipeline.executar()

    if resultado.erros:
        caminho_falhas = Path(caminho_csv).with_name(
            f"{Path(caminho_csv).stem}_falhas.csv"
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
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
