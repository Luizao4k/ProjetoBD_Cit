"""
Protocols (interfaces estruturais) do pipeline de importação.

Usar Protocol em vez de ABC é intencional: nenhuma implementação
concreta (CsvReader, EscolaMapper, CriarEscolaUseCase, ...) precisa
herdar de nada daqui. Elas só precisam ter os métodos com a
assinatura certa — inclusive os Use Cases que já existiam antes desse
desenho, sem precisar tocar num arquivo sequer da camada de aplicação.
Isso é o que torna o Pipeline capaz de reutilizar CriarEscolaUseCase,
CriarDreUseCase etc. tal como já estão escritos.
"""

from __future__ import annotations

from typing import Iterator, Protocol, TypeVar, runtime_checkable

LinhaBruta = dict[str, str]
"""O formato que qualquer Reader entrega: nomes de coluna -> texto cru."""

# Variância declarada explicitamente porque cada TypeVar só aparece de
# UM lado da assinatura em cada Protocol: Mapper só PRODUZ T (nunca o
# recebe como argumento) -> covariante. UseCase CONSOME TEntrada
# (contravariante) e PRODUZ TSaida (covariante). Sem isso, mypy rejeita
# os Protocols (variância errada pro uso) — não é só formalismo: é o
# que garante que Mapper[Escola] possa ser usado onde Mapper[object]
# é esperado, com segurança.
TEntrada_co = TypeVar("TEntrada_co", covariant=True)
TEntrada_contra = TypeVar("TEntrada_contra", contravariant=True)
TSaida_co = TypeVar("TSaida_co", covariant=True)


@runtime_checkable
class Reader(Protocol):
    """
    Uma fonte de linhas brutas, uma por vez.

    Implementações NÃO fazem parsing de tipos nem validação — isso é
    trabalho de Conversor e Mapper. Um Reader só sabe ler.
    `total_estimado` é opcional (pode devolver None): serve só para
    o ProgressTracker mostrar "processado X de Y"; nenhuma
    implementação é obrigada a saber o total sem quebrar o streaming.
    """

    def ler(self) -> Iterator[LinhaBruta]:
        """Produz uma LinhaBruta por vez. Deve ser um gerador (yield),
        nunca materializar a fonte inteira numa lista."""
        ...

    def total_estimado(self) -> int | None:
        """Quantidade aproximada de registros, se for barato calcular
        sem carregar tudo em memória. None se não for possível saber."""
        ...

    def validar(self) -> list[str]:
        """
        Checagens estruturais antes de começar a ler (arquivo existe,
        colunas obrigatórias presentes etc.). Devolve uma lista de
        problemas — vazia significa "pode prosseguir". O Pipeline
        interrompe ANTES de processar qualquer linha se isso não
        vier vazio; não faz sentido processar 50 mil linhas pra só
        então descobrir que faltava uma coluna inteira.
        """
        ...


@runtime_checkable
class Mapper(Protocol[TSaida_co]):
    """
    Converte uma LinhaBruta num DTO de entrada de Use Case.

    Pode usar os Conversores (str -> int, str -> bool, str -> date)
    e pode depender de Repositories para resolver chaves estrangeiras
    por um identificador amigável (ex: inep em vez de escola_id).
    NUNCA deve validar regra de negócio — "nome não pode ser vazio",
    "quantidade tem que ser positiva" são checagens dos Value
    Objects, disparadas quando o Use Case constrói a entidade.
    """

    def mapear(self, linha: LinhaBruta) -> TSaida_co: ...


@runtime_checkable
class UseCase(Protocol[TEntrada_contra, TSaida_co]):
    """
    Qualquer caso de uso com a forma `executar(dados) -> saida`.

    Todo CriarXUseCase da camada de aplicação já satisfaz este
    protocolo sem herdar de nada — Protocol é estrutural (duck
    typing verificado estaticamente). É isso que permite o Pipeline
    reutilizar o Use Case exatamente como ele já existe.
    """

    def executar(self, dados: TEntrada_contra) -> TSaida_co: ...


@runtime_checkable
class GerenciadorDeTransacao(Protocol):
    """
    Abstrai a decisão de confirmar/desfazer uma escrita.

    Desde que os repositórios pararam de comitar sozinhos a cada
    escrita (ver infrastructure/database/sqlite/_util.py), alguém
    precisa decidir quando uma linha bem-sucedida se torna permanente.
    Sem este Protocol, o Pipeline precisaria importar sqlite3
    diretamente pra chamar commit/rollback — quebrando a mesma
    independência de infraestrutura que Reader/Mapper/UseCase já têm.
    Opcional: um Pipeline sem gerenciador (o padrão) simplesmente não
    confirma nada sozinho, como sempre foi nos testes com dublês.
    """

    def confirmar(self) -> None: ...
    def desfazer(self) -> None: ...
