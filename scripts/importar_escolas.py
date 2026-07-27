"""
Importa Escolas em lote a partir de um CSV.

Uso (a partir da raiz do projeto):
    python -m scripts.importar_escolas caminho/para/escolas.csv [caminho/do/banco.db]

Colunas esperadas no CSV (cabeçalho):
    inep, nome, tipo, municipio, endereco, dre_id, dre_nome

- endereco é opcional (pode vir vazio).
- a DRE pode ser informada por dre_id OU por dre_nome — se dre_id vier
  preenchido, ele é usado direto; senão, dre_nome é procurado entre as
  DREs já cadastradas no banco. Pelo menos uma das duas é obrigatória.

Linhas que falharem (INEP duplicado, DRE não encontrada, dado
inválido, coluna faltante, etc.) NÃO interrompem a importação: são
registradas com o motivo e gravadas num CSV de falhas ao lado do
arquivo de entrada (<nome_do_arquivo>_falhas.csv), pra análise e
reimportação depois de corrigidas. As demais linhas continuam sendo
processadas normalmente.
"""

from __future__ import annotations

import sys
from pathlib import Path

from domain.repositories import DreRepository
from domain.value_objects import Nome
from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
)
from application.use_cases.escola import CriarEscolaUseCase, CriarEscolaInput

from scripts._importador_util import (
    ler_csv,
    importar_em_lote,
    exportar_falhas_csv,
)


def resolver_dre_id(linha: dict[str, str], repo_dre: DreRepository) -> int:
    """
    Resolve o dre_id da linha, aceitando dre_id direto ou dre_nome.
    Levanta ValueError com uma mensagem clara se não conseguir —
    o importador captura isso e registra a linha como falha.
    """
    dre_id_bruto = (linha.get("dre_id") or "").strip()
    if dre_id_bruto:
        return int(dre_id_bruto)

    nome_dre = (linha.get("dre_nome") or "").strip()
    if not nome_dre:
        raise ValueError("Linha não informou nem dre_id nem dre_nome.")

    encontradas = repo_dre.buscar_por_nome(Nome(nome_dre))

    if not encontradas:
        raise ValueError(f"DRE '{nome_dre}' não encontrada entre as DREs cadastradas.")
    if len(encontradas) > 1:
        raise ValueError(
            f"Mais de uma DRE encontrada com o nome '{nome_dre}' — informe dre_id."
        )
    return encontradas[0].id


def montar_entrada_escola(
    linha: dict[str, str], repo_dre: DreRepository
) -> CriarEscolaInput:
    """
    Converte uma linha crua do CSV no Input DTO de CriarEscolaUseCase.
    Qualquer KeyError (coluna faltante) ou ValueError (DRE não
    resolvida) sobe pra ser capturado pelo importar_em_lote.
    """
    dre_id = resolver_dre_id(linha, repo_dre)
    endereco = (linha.get("endereco") or "").strip() or None

    return CriarEscolaInput(
        inep=linha["inep"].strip(),
        nome=linha["nome"].strip(),
        tipo=linha["tipo"].strip().upper(),
        municipio=linha["municipio"].strip(),
        dre_id=dre_id,
        endereco=endereco,
    )


def importar_escolas(caminho_csv: str | Path, caminho_banco: str = "escolas.db") -> None:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_dre = SqliteDreRepository(conexao)
    repo_escola = SqliteEscolaRepository(conexao)
    caso_de_uso = CriarEscolaUseCase(repo_escola)

    linhas = ler_csv(caminho_csv)

    resultado = importar_em_lote(
        linhas,
        montar_entrada=lambda linha: montar_entrada_escola(linha, repo_dre),
        executar=caso_de_uso.executar,
    )

    print(resultado.resumo())

    if resultado.falhas:
        caminho_entrada = Path(caminho_csv)
        caminho_falhas = caminho_entrada.with_name(
            f"{caminho_entrada.stem}_falhas.csv"
        )
        exportar_falhas_csv(resultado, caminho_falhas)
        print(f"Falhas gravadas em: {caminho_falhas}")
        for falha in resultado.falhas:
            print(
                f"  linha {falha.numero_linha}: {falha.tipo_erro} — {falha.motivo}"
            )

    conexao.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/importar_escolas.py caminho/para/escolas.csv [banco.db]")
        sys.exit(1)

    caminho_csv_arg = sys.argv[1]
    caminho_banco_arg = sys.argv[2] if len(sys.argv) > 2 else "escolas.db"
    importar_escolas(caminho_csv_arg, caminho_banco_arg)
