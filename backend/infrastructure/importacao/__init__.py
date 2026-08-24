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

from backend.infrastructure.importacao.pipeline import ArquivoInvalidoError, ImportadorPipeline
from backend.infrastructure.importacao.resultado import ResultadoImportacao
from backend.infrastructure.importacao.erro import ErroImportacao
from backend.infrastructure.importacao.protocolos import GerenciadorDeTransacao
from backend.infrastructure.importacao.progresso import (
    ProgressTracker,
    ProgressTrackerConsole,
    ProgressTrackerSilencioso,
)
from backend.infrastructure.importacao.log_alteracao import LogAlteracao, MudancaCampo, RegistroAlteracao

__all__ = [
    "ImportadorPipeline",
    "ArquivoInvalidoError",
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
