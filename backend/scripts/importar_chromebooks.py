"""
Importa registros de Chromebook em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_chromebooks caminho/para/chromebooks.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    kit_aluno, kit_professor (opcionais; se vierem, precisam ser
    números inteiros positivos)
    escola_id OU escola_inep (pelo menos uma)

Cada escola só pode ter um registro de Chromebook (1:1 no schema) —
uma segunda linha para a mesma escola falha com "escola já possui
Chromebook".

Ordem de importação: rode depois de scripts.importar_escolas.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteChromebookRepository,
    SqliteEscolaRepository,
)
from application.use_cases.chromebook import CriarChromebookUseCase

from infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import CsvReader
from infrastructure.importacao.mappers import ChromebookMapper


def importar_chromebooks(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_escola = SqliteEscolaRepository(conexao)
    repo_chromebook = SqliteChromebookRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=ChromebookMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=ChromebookMapper(repo_escola),
        use_case=CriarChromebookUseCase(repo_chromebook),
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
            "Uso: python -m scripts.importar_chromebooks caminho/para/chromebooks.csv [banco.db]"
        )
        sys.exit(1)

    try:
        importar_chromebooks(
            sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
        )
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
