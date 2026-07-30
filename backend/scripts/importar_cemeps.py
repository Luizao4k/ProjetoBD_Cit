"""
Importa CEMEPs em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_cemeps caminho/para/cemeps.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    comentario (opcional)
    escola_id OU escola_inep (pelo menos uma)

Cada escola só pode ter um CEMEP (1:1 no schema) — uma segunda linha
para a mesma escola falha com "escola já possui CEMEP".

Ordem de importação: rode depois de scripts.importar_escolas.
scripts.importar_responsaveis depende deste (Responsável referencia
o CEMEP pelo escola_inep da escola a que ele pertence).
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteCemepRepository,
    SqliteEscolaRepository,
)
from application.use_cases.cemep import CriarCemepUseCase

from infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import CsvReader
from infrastructure.importacao.mappers import CemepMapper


def importar_cemeps(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_escola = SqliteEscolaRepository(conexao)
    repo_cemep = SqliteCemepRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=CemepMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=CemepMapper(repo_escola),
        use_case=CriarCemepUseCase(repo_cemep),
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
        print("Uso: python -m scripts.importar_cemeps caminho/para/cemeps.csv [banco.db]")
        sys.exit(1)

    try:
        importar_cemeps(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db")
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
