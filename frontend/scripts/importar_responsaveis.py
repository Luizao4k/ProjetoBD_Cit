"""
Importa Responsáveis em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_responsaveis caminho/para/responsaveis.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    nome (obrigatória)
    cemep_id OU escola_inep (pelo menos uma — CEMEP não tem nome
    próprio, então escola_inep é a forma amigável de identificá-lo,
    através da escola a que pertence)

Um CEMEP pode ter vários responsáveis (1:N) — não há restrição de
unicidade de cemep_id no schema.

Ordem de importação: rode depois de scripts.importar_cemeps — este
importador resolve cemep_id (via escola_inep) contra CEMEPs já
cadastrados no banco. scripts.importar_turmas_cemep depende deste.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteCemepRepository,
    SqliteEscolaRepository,
    SqliteResponsavelRepository,
)
from application.use_cases.responsavel import CriarResponsavelUseCase

from importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from importacao.readers import CsvReader
from importacao.mappers import ResponsavelMapper


def importar_responsaveis(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_escola = SqliteEscolaRepository(conexao)
    repo_cemep = SqliteCemepRepository(conexao)
    repo_responsavel = SqliteResponsavelRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=ResponsavelMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=ResponsavelMapper(repo_cemep, repo_escola),
        use_case=CriarResponsavelUseCase(repo_responsavel),
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
        print(
            "Uso: python -m scripts.importar_responsaveis caminho/para/responsaveis.csv [banco.db]"
        )
        sys.exit(1)

    try:
        importar_responsaveis(
            sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
        )
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
