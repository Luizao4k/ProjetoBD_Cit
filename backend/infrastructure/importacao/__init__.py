"""
Infraestrutura genérica de importação em lote (Fase 4 do roadmap).

Ponto de entrada: ImportadorPipeline. Cada entidade (DRE, Escola,
Diretor, CEMEP, Chromebook, Responsável, Turma CEMEP, Starlink) só
precisa fornecer um Reader, um Mapper e um Use Case já existente —
o algoritmo de leitura em streaming, captura de erro, progresso e
relatório final existe uma única vez, em pipeline.py.

Ver scripts/importar_*.py para a composição concreta de cada
entidade.
"""

from infrastructure.importacao.pipeline import EntradaImportacaoInvalidaError, ImportadorPipeline
from infrastructure.importacao.resultado import ResultadoImportacao
from infrastructure.importacao.erro import ErroImportacao
from infrastructure.importacao.protocolos import GerenciadorDeTransacao
from infrastructure.importacao.progresso import (
    ProgressTracker,
    ProgressTrackerConsole,
    ProgressTrackerSilencioso,
)
from infrastructure.importacao.log_alteracao import LogAlteracao, MudancaCampo, RegistroAlteracao

__all__ = [
    "ImportadorPipeline",
    "EntradaImportacaoInvalidaError",
    "ResultadoImportacao",
    "ErroImportacao",
    "GerenciadorDeTransacao",
    "ProgressTracker",
    "ProgressTrackerConsole",
    "ProgressTrackerSilencioso",
    "LogAlteracao",
    "MudancaCampo",
    "RegistroAlteracao",
]
