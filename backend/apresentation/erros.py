"""
Tratamento global de exceções: mapeia a hierarquia de
shared.exceptions para respostas HTTP em JSON.

Registrado uma única vez, em criar_app() — nenhum controller precisa
de try/except: uma exceção de domínio/aplicação/infraestrutura sobe
naturalmente até aqui.
"""

from __future__ import annotations

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from shared.exceptions import (
    ApplicationError,
    CemepPossuiResponsaveisError,
    DomainError,
    DrePossuiEscolasError,
    EscolaPossuiChromebookError,
    EscolaPossuiCemepError,
    EscolaPossuiDiretorError,
    EscolaPossuiStarlinksError,
    InfrastructureError,
    RegistroDuplicadoError,
    RegistroNaoEncontradoError,
    RelacaoNaoEncontradaError,
    ResponsavelPossuiTurmasError,
)

# Estas 7 herdam de PersistenciaError (InfrastructureError) por
# nascerem de uma FK-violation no SQLite, mas semanticamente NÃO são
# uma falha de infraestrutura: são o cliente tentando remover um
# registro que ainda tem dependentes. Por isso viram 409 (conflito de
# estado), não 500. Se um dia existir uma classe-base própria pra
# "restrição de integridade referencial" na hierarquia de exceções,
# esta lista vira um único isinstance — hoje precisa ser explícita.
_CONFLITOS_DE_INTEGRIDADE_REFERENCIAL: tuple[type[Exception], ...] = (
    CemepPossuiResponsaveisError,
    DrePossuiEscolasError,
    ResponsavelPossuiTurmasError,
    EscolaPossuiDiretorError,
    EscolaPossuiCemepError,
    EscolaPossuiChromebookError,
    EscolaPossuiStarlinksError,
)


def _corpo(excecao: Exception) -> dict[str, str]:
    return {"erro": type(excecao).__name__, "mensagem": str(excecao)}


def registrar_tratadores_de_erro(app: Flask) -> None:
    """
    Flask escolhe o handler mais específico na MRO da exceção
    levantada automaticamente — a ordem de registro abaixo não afeta
    o comportamento, só a legibilidade (do mais específico ao mais
    genérico).
    """

    for classe in _CONFLITOS_DE_INTEGRIDADE_REFERENCIAL:
        app.register_error_handler(
            classe, lambda exc: (jsonify(_corpo(exc)), 409)
        )

    @app.errorhandler(RegistroDuplicadoError)
    def _duplicado(exc: RegistroDuplicadoError):
        return jsonify(_corpo(exc)), 409

    @app.errorhandler(RegistroNaoEncontradoError)
    def _nao_encontrado(exc: RegistroNaoEncontradoError):
        return jsonify(_corpo(exc)), 404

    @app.errorhandler(RelacaoNaoEncontradaError)
    def _relacao_ausente(exc: RelacaoNaoEncontradaError):
        return jsonify(_corpo(exc)), 404

    @app.errorhandler(DomainError)
    def _dominio(exc: DomainError):
        # Nome/Telefone/Email/Município/Endereço/Inep/Quantidade/
        # Comentário inválidos — o cliente mandou um dado malformado.
        return jsonify(_corpo(exc)), 400

    @app.errorhandler(ApplicationError)
    def _aplicacao(exc: ApplicationError):
        # Rede de segurança para qualquer ApplicationError que não
        # seja RegistroDuplicado/NaoEncontrado/RelacaoNaoEncontrada —
        # nenhuma existe hoje fora dessas três, mas uma futura cairia
        # aqui em vez de virar 500.
        return jsonify(_corpo(exc)), 400

    @app.errorhandler(InfrastructureError)
    def _infraestrutura(exc: InfrastructureError):
        return jsonify(_corpo(exc)), 500

    @app.errorhandler(ValueError)
    def _valor_invalido(exc: ValueError):
        # Caso específico, não uma rede de segurança genérica: os Use
        # Cases constroem TipoEscola(dados.tipo) diretamente de um
        # Enum do stdlib, que levanta ValueError puro (não uma
        # exceção de domínio própria) para um valor fora de
        # ESTADUAL/MUNICIPAL. É a única fonte de ValueError conhecida
        # nesse caminho — os Value Objects (Nome, Telefone, Inep...)
        # já têm suas próprias exceções, cobertas por DomainError
        # acima.
        return jsonify(_corpo(exc)), 400

    @app.errorhandler(HTTPException)
    def _http(exc: HTTPException):
        # Normaliza os erros do próprio Flask/Werkzeug (404 de rota
        # inexistente, 405 de método errado, 400 de JSON malformado)
        # pro mesmo formato — a API nunca devolve a página HTML padrão
        # de erro.
        return jsonify({"erro": exc.name, "mensagem": exc.description}), exc.code
