"""
Orquestrador da Importação Inicial: roda os 8 importadores, na ordem
de dependência correta, com um único comando.

Uso (a partir da raiz do projeto):
    python -m scripts.importar_tudo caminho/para/diretorio [caminho/do/banco.db]

Espera um diretório contendo arquivos nomeados por entidade — CSV ou
Excel, escolhido automaticamente por extensão (ver
importacao.readers.criar_reader):

    dres.csv / dres.xlsx
    escolas.csv / escolas.xlsx
    diretores.csv / diretores.xlsx
    cemeps.csv / cemeps.xlsx
    chromebooks.csv / chromebooks.xlsx
    starlinks.csv / starlinks.xlsx
    responsaveis.csv / responsaveis.xlsx
    turmas_cemep.csv / turmas_cemep.xlsx

Entidade sem arquivo correspondente no diretório é pulada (com aviso
no relatório) — nem todo projeto vai ter dado de Starlink, por
exemplo, e isso não deveria impedir importar o resto.

A ordem abaixo não é arbitrária, é a mesma cadeia de dependência
provada por teste em tests/test_importacao/test_scripts_integracao.py
(test_cadeia_completa_dre_at_turma_via_scripts_independentes):

    DRE
      -> Escola
           -> Diretor   (só depende de Escola)
           -> CEMEP     (só depende de Escola)
             -> Responsável  (depende de CEMEP)
               -> Turma CEMEP  (depende de Responsável)
           -> Chromebook (só depende de Escola)
           -> Starlink   (só depende de Escola)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from infrastructure.importacao import EntradaImportacaoInvalidaError, ResultadoImportacao
from scripts.importar_dres import importar_dres
from scripts.importar_escolas import importar_escolas
from scripts.importar_diretores import importar_diretores
from scripts.importar_cemeps import importar_cemeps
from scripts.importar_chromebooks import importar_chromebooks
from scripts.importar_starlinks import importar_starlinks
from scripts.importar_responsaveis import importar_responsaveis
from scripts.importar_turmas_cemep import importar_turmas_cemep

FuncaoImportar = Callable[..., ResultadoImportacao]

_EXTENSOES_SUPORTADAS = (".csv", ".xlsx", ".xlsm")


@dataclass(frozen=True)
class _EntradaOrquestracao:
    nome_entidade: str
    nome_base_arquivo: str
    funcao_importar: FuncaoImportar


_ORDEM_DE_IMPORTACAO: list[_EntradaOrquestracao] = [
    _EntradaOrquestracao("DRE", "dres", importar_dres),
    _EntradaOrquestracao("Escola", "escolas", importar_escolas),
    _EntradaOrquestracao("Diretor", "diretores", importar_diretores),
    _EntradaOrquestracao("CEMEP", "cemeps", importar_cemeps),
    _EntradaOrquestracao("Chromebook", "chromebooks", importar_chromebooks),
    _EntradaOrquestracao("Starlink", "starlinks", importar_starlinks),
    _EntradaOrquestracao("Responsável", "responsaveis", importar_responsaveis),
    _EntradaOrquestracao("Turma CEMEP", "turmas_cemep", importar_turmas_cemep),
]


@dataclass
class _ResultadoEntidade:
    nome_entidade: str
    arquivo: Path | None
    resultado: ResultadoImportacao | None = None
    erro_arquivo: str | None = None


def _localizar_arquivo(diretorio: Path, nome_base: str) -> Path | None:
    """CSV tem preferência se, por algum motivo, existirem os dois
    formatos pra mesma entidade no diretório — critério de desempate
    simples, não uma checagem de ambiguidade."""
    for extensao in _EXTENSOES_SUPORTADAS:
        candidato = diretorio / f"{nome_base}{extensao}"
        if candidato.exists():
            return candidato
    return None


def importar_tudo(
    diretorio: str | Path, caminho_banco: str = "escolas.db"
) -> list[_ResultadoEntidade]:
    diretorio_path = Path(diretorio)
    relatorios: list[_ResultadoEntidade] = []

    for entrada in _ORDEM_DE_IMPORTACAO:
        arquivo = _localizar_arquivo(diretorio_path, entrada.nome_base_arquivo)

        if arquivo is None:
            print(
                f"[{entrada.nome_entidade}] arquivo não encontrado "
                f"({entrada.nome_base_arquivo}.csv/.xlsx) — pulando."
            )
            relatorios.append(_ResultadoEntidade(entrada.nome_entidade, None))
            continue

        print(f"\n[{entrada.nome_entidade}] importando de {arquivo.name}...")
        try:
            resultado = entrada.funcao_importar(arquivo, caminho_banco)
            relatorios.append(
                _ResultadoEntidade(entrada.nome_entidade, arquivo, resultado)
            )
        except EntradaImportacaoInvalidaError as erro:
            print(f"[{entrada.nome_entidade}] arquivo inválido: {erro}")
            relatorios.append(
                _ResultadoEntidade(
                    entrada.nome_entidade, arquivo, erro_arquivo=str(erro)
                )
            )

    _imprimir_relatorio_final(relatorios)
    return relatorios


def _imprimir_relatorio_final(relatorios: list[_ResultadoEntidade]) -> None:
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL DA IMPORTAÇÃO")
    print("=" * 60)

    total_sucessos = 0
    total_erros = 0

    for item in relatorios:
        if item.resultado is None:
            status = (
                "arquivo não encontrado, pulado"
                if item.erro_arquivo is None
                else f"arquivo inválido: {item.erro_arquivo}"
            )
            print(f"  {item.nome_entidade:<15} {status}")
            continue

        total_sucessos += len(item.resultado.sucessos)
        total_erros += len(item.resultado.erros)
        print(
            f"  {item.nome_entidade:<15} "
            f"{len(item.resultado.sucessos)} sucesso(s), "
            f"{len(item.resultado.erros)} falha(s)"
        )

    print("-" * 60)
    print(f"  TOTAL: {total_sucessos} registro(s) importado(s), {total_erros} falha(s)")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Uso: python -m scripts.importar_tudo caminho/para/diretorio [banco.db]"
        )
        nomes = ", ".join(f"{e.nome_base_arquivo}.csv/.xlsx" for e in _ORDEM_DE_IMPORTACAO)
        print(f"Espera arquivos nomeados: {nomes}")
        sys.exit(1)

    importar_tudo(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "escolas.db")
