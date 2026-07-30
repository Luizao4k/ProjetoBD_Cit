"""
Importa Turmas de CEMEP em lote a partir de um CSV, usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_turmas_cemep caminho/para/turmas.csv [caminho/do/banco.db]

Colunas esperadas no CSV:
    nome_turma, responsavel_id (ambas obrigatórias)

Diferente dos demais importadores, aqui só é aceito responsavel_id
direto — não há busca por nome de responsável disponível no
repositório (ver TurmaCemepMapper para a justificativa completa).

Um responsável pode ter várias turmas (1:N) — não há restrição de
unicidade de responsavel_id no schema.

Ordem de importação: último da cadeia — rode depois de
scripts.importar_responsaveis.
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import SqliteTurmaCemepRepository
from application.use_cases.turma_cemep import CriarTurmaCemepUseCase

from infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from infrastructure.importacao.readers import CsvReader
from infrastructure.importacao.mappers import TurmaCemepMapper


def importar_turmas_cemep(
    caminho_csv: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_turma = SqliteTurmaCemepRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(
            caminho_csv, colunas_obrigatorias=TurmaCemepMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=TurmaCemepMapper(),
        use_case=CriarTurmaCemepUseCase(repo_turma),
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
            "Uso: python -m scripts.importar_turmas_cemep caminho/para/turmas.csv [banco.db]"
        )
        sys.exit(1)

    try:
        importar_turmas_cemep(
            sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
        )
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
