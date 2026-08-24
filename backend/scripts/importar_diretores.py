"""
Importa Diretores em lote a partir de um CSV ou Excel (.xlsx/.xlsm), usando o
ImportadorPipeline genérico (ver importacao/pipeline.py).

Uso (a partir da raiz do projeto):
    python -m scripts.importar_diretores caminho/para/diretores.csv [caminho/do/banco.db]

O formato é escolhido automaticamente pela extensão do
arquivo (ver importacao.readers.criar_reader).

Colunas esperadas:
    nome (obrigatória)
    telefone, email (opcionais)
    escola_id OU escola_inep (pelo menos uma)

Cada escola só pode ter um diretor (1:1 no schema) — uma segunda
linha para a mesma escola falha com "escola já possui diretor".

Ordem de importação: rode depois de scripts.importar_escolas — este
importador resolve escola_id contra escolas já cadastradas no banco.
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
    SqliteDiretorRepository,
    SqliteEscolaRepository,
)
from application.use_cases.diretor import CriarDiretorUseCase

from backend.infrastructure.importacao import ArquivoInvalidoError, ImportadorPipeline, ResultadoImportacao
from backend.infrastructure.importacao.readers import criar_reader
from backend.infrastructure.importacao.mappers import DiretorMapper


def importar_diretores(
    caminho_arquivo: str | Path, caminho_banco: str = "escolas.db"
) -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_escola = SqliteEscolaRepository(conexao)
    repo_diretor = SqliteDiretorRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=criar_reader(
            caminho_arquivo, colunas_obrigatorias=DiretorMapper.COLUNAS_OBRIGATORIAS
        ),
        mapper=DiretorMapper(repo_escola),
        use_case=CriarDiretorUseCase(repo_diretor),
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
        print(
            "Uso: python -m scripts.importar_diretores caminho/para/diretores.csv [banco.db]"
        )
        sys.exit(1)

    try:
        importar_diretores(
            sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
        )
    except ArquivoInvalidoError as erro:
        print(f"Arquivo inválido: {erro}", file=sys.stderr)
        sys.exit(1)
