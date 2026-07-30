"""
ImportadorPipeline: o algoritmo de importação em lote, escrito uma
única vez e reutilizado por todas as entidades.

Segue o fluxo:

    Validação do arquivo
        -> Reader (streaming)
        -> Mapper (linha crua -> DTO)
        -> Use Case (DTO -> entidade de domínio, via Repository)
        -> ResultadoImportacao

Cada entidade só fornece Reader + Mapper + Use Case (Dependency
Injection via construtor); o loop, o streaming, o progresso e a
captura de erro moram exclusivamente aqui.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from importacao.log_alteracao import LogAlteracao
from importacao.progresso import ProgressTracker, ProgressTrackerConsole
from importacao.protocolos import Mapper, Reader, UseCase
from importacao.erro import ErroImportacao
from importacao.resultado import ResultadoImportacao

# TypeVars próprios da classe concreta (invariantes, o padrão): os
# TEntrada_co/TEntrada_contra/TSaida_co de protocolos.py existem só
# para as declarações dos Protocols em si. Aqui o que amarra "o Mapper
# produz o mesmo tipo que o UseCase consome" é a MESMA instância de
# TEntrada aparecendo nos dois parâmetros do __init__ — variância não
# entra em jogo numa classe concreta (não-Protocol).
TEntrada = TypeVar("TEntrada")
TSaida = TypeVar("TSaida")


class ArquivoInvalidoError(Exception):
    """Levantada quando reader.validar() aponta problemas estruturais
    (arquivo ausente, coluna obrigatória faltando etc.) — decisão
    deliberada de interromper ANTES da primeira linha: não faz sentido
    processar um arquivo de 50 mil linhas pra só então descobrir que
    faltava uma coluna inteira."""

    def __init__(self, problemas: list[str]) -> None:
        self.problemas = problemas
        super().__init__("; ".join(problemas))


class ImportadorPipeline(Generic[TEntrada, TSaida]):
    """
    Orquestra a importação em lote de UMA entidade.

    Não conhece regra de negócio alguma — não sabe o que é um INEP,
    o que é uma DRE, nem que "quantidade" precisa ser positiva. Só
    sabe: validar o arquivo, ler em streaming, mapear, executar,
    capturar exceção linha a linha, reportar progresso e agregar um
    resultado. Toda regra de negócio continua exclusivamente nos
    Value Objects e nos Use Cases, na camada de aplicação/domínio.

    Genérica em TEntrada (o DTO que o Mapper produz) e TSaida (o que
    o Use Case devolve) — é assim que `ImportadorPipeline(mapper=
    EscolaMapper(...), use_case=CriarEscolaUseCase(...)).executar()`
    tem seu retorno inferido como `ResultadoImportacao[EscolaOutput]`
    pelo type checker, sem precisar de anotação manual em cada script.

    Uso:
        pipeline = ImportadorPipeline(
            reader=CsvReader("escolas.csv"),
            mapper=EscolaMapper(repo_dre),
            use_case=CriarEscolaUseCase(repo_escola),
        )
        resultado = pipeline.executar()
    """

    def __init__(
        self,
        reader: Reader,
        mapper: Mapper[TEntrada],
        use_case: UseCase[TEntrada, TSaida],
        progress_tracker: ProgressTracker | None = None,
        log_alteracao: LogAlteracao | None = None,
    ) -> None:
        self._reader = reader
        self._mapper = mapper
        self._use_case = use_case
        self._progress = progress_tracker or ProgressTrackerConsole()
        self.log_alteracao = log_alteracao

    def executar(self) -> ResultadoImportacao[TSaida]:
        problemas = self._reader.validar()
        if problemas:
            raise ArquivoInvalidoError(problemas)

        resultado: ResultadoImportacao[TSaida] = ResultadoImportacao()
        total = self._reader.total_estimado()

        processados = 0
        for linha in self._reader.ler():
            processados += 1

            try:
                dto = self._mapper.mapear(linha)
                saida = self._use_case.executar(dto)
                resultado.registrar_sucesso(saida)

            except Exception as excecao:
                # Captura ampla e deliberada: uma linha ruim (coluna
                # faltante -> KeyError; VO inválido -> XInvalidoError;
                # violação de integridade -> PersistenciaError; FK não
                # resolvida -> ValueError do próprio Mapper) NUNCA pode
                # derrubar as linhas seguintes. O erro não é engolido:
                # vira um ErroImportacao rastreável no resultado final.
                erro = ErroImportacao.a_partir_de(
                    numero_linha=processados,
                    dados_originais=linha,
                    excecao=excecao,
                )
                resultado.registrar_erro(erro)

            self._progress.atualizar(processados, total)

        self._progress.finalizar(resultado)
        return resultado
