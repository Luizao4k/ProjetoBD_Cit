"""
Importa DREs em lote a partir de um CSV, usando o ImportadorPipeline
genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_dres caminho/para/dres.csv [caminho/do/banco.db]

Colunas esperadas no CSV: nome (obrigatória), telefone (opcional).

DRE não tem restrição de unicidade de nome no banco — duas DREs podem
ter o mesmo nome (ex: reestruturação administrativa); este importador
não barra duplicatas de nome.

Ordem de importação: primeiro importador da cadeia — nenhuma outra
entidade depende de mais nada, mas o importador de Escola depende de
DREs já existirem no banco.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import SqliteDreRepository
from application.use_cases.dre import CriarDreUseCase

from infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import CsvReader
from infrastructure.importacao.mappers import DreMapper


def importar_dres(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_dre = SqliteDreRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=DreMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=DreMapper(),
        use_case=CriarDreUseCase(repo_dre),
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
        print("Uso: python -m scripts.importar_dres caminho/para/dres.csv [banco.db]")
        sys.exit(1)

    try:
        importar_dres(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db")
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
