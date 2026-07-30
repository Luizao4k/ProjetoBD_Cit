"""
Importa designações de Starlink em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_starlinks caminho/para/starlinks.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    designacao (obrigatória)
    escola_id OU escola_inep (pelo menos uma)

Diferente de Diretor/CEMEP/Chromebook, uma escola PODE ter várias
designações de Starlink — não há restrição de unicidade de escola_id
no schema.

Ordem de importação: rode depois de scripts.importar_escolas.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteEscolaRepository,
    SqliteStarlinkRepository,
)
from application.use_cases.starlink import CriarStarlinkUseCase

from importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from importacao.readers import CsvReader
from importacao.mappers import StarlinkMapper


def importar_starlinks(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_escola = SqliteEscolaRepository(conexao)
    repo_starlink = SqliteStarlinkRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=StarlinkMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=StarlinkMapper(repo_escola),
        use_case=CriarStarlinkUseCase(repo_starlink),
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
            "Uso: python -m scripts.importar_starlinks caminho/para/starlinks.csv [banco.db]"
        )
        sys.exit(1)

    try:
        importar_starlinks(
            sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
        )
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
