"""
Testes do ImportadorPipeline usando dublês de Reader/Mapper/UseCase
— nada de domínio real aqui de propósito: o pipeline não deveria
precisar de uma Escola ou uma DRE existir pra ter seu algoritmo
testado. Os testes com entidades reais (test_importar_*.py) cobrem a
composição concreta.
"""

import pytest

from backend.infrastructure.importacao import (
    ArquivoInvalidoError,
    ImportadorPipeline,
    ProgressTrackerSilencioso,
)


class ReaderFalso:
    """Produz as linhas dadas no construtor, uma por vez (via yield —
    então também serve pra provar que o Pipeline consome um
    generator, não uma lista pré-carregada)."""

    def __init__(self, linhas, problemas_validacao=None):
        self._linhas = linhas
        self._problemas = problemas_validacao or []

    def ler(self):
        for linha in self._linhas:
            yield linha

    def total_estimado(self):
        return len(self._linhas)

    def validar(self):
        return self._problemas


class MapperDobraValor:
    """Mapper de teste: espera {"valor": "N"} e devolve N*2 como
    'DTO'. Se "valor" não for um inteiro, deixa o ValueError
    propagar — é exatamente assim que um Mapper real se comporta."""

    def mapear(self, linha):
        return int(linha["valor"]) * 2


class UseCaseFalha3:
    """Use Case de teste: recusa o valor 3, aceita qualquer outro
    (devolve o próprio valor como 'saída')."""

    def executar(self, dado):
        if dado == 6:  # 3 * 2, vindo do Mapper
            raise ValueError("valor 3 não é permitido (regra de teste)")
        return dado


class GerenciadorDeTransacaoFalso:
    """Dublê que só registra quando confirmar()/desfazer() foram
    chamados, na ordem em que aconteceram."""

    def __init__(self):
        self.chamadas = []

    def confirmar(self):
        self.chamadas.append("confirmar")

    def desfazer(self):
        self.chamadas.append("desfazer")


def _pipeline(linhas, problemas_validacao=None, gerenciador_transacao=None):
    return ImportadorPipeline(
        reader=ReaderFalso(linhas, problemas_validacao),
        mapper=MapperDobraValor(),
        use_case=UseCaseFalha3(),
        progress_tracker=ProgressTrackerSilencioso(),
        gerenciador_transacao=gerenciador_transacao,
    )


def test_pipeline_processa_todas_as_linhas_com_sucesso():
    linhas = [{"valor": "1"}, {"valor": "2"}, {"valor": "4"}]

    resultado = _pipeline(linhas).executar()

    assert resultado.sucessos == [2, 4, 8]
    assert resultado.erros == []


def test_pipeline_continua_apos_erro_de_use_case_em_uma_linha():
    linhas = [{"valor": "1"}, {"valor": "3"}, {"valor": "5"}]

    resultado = _pipeline(linhas).executar()

    assert resultado.sucessos == [2, 10]  # 1*2 e 5*2 -- a linha do 3 falhou
    assert len(resultado.erros) == 1
    assert resultado.erros[0].numero_linha == 2
    assert resultado.erros[0].tipo_erro == "ValueError"
    assert resultado.erros[0].dados_originais == {"valor": "3"}


def test_pipeline_continua_apos_erro_de_mapper_coluna_faltante():
    linhas = [{"valor": "1"}, {"outra_coluna": "x"}, {"valor": "2"}]

    resultado = _pipeline(linhas).executar()

    assert resultado.sucessos == [2, 4]
    assert len(resultado.erros) == 1
    assert resultado.erros[0].tipo_erro == "KeyError"
    assert resultado.erros[0].numero_linha == 2


def test_pipeline_levanta_arquivo_invalido_antes_de_processar_qualquer_linha():
    linhas_que_nunca_deveriam_ser_lidas = [{"valor": "1"}]

    pipeline = _pipeline(
        linhas_que_nunca_deveriam_ser_lidas,
        problemas_validacao=["coluna 'valor' ausente no cabeçalho"],
    )

    with pytest.raises(ArquivoInvalidoError) as exc_info:
        pipeline.executar()

    assert "coluna 'valor' ausente" in str(exc_info.value)


def test_resultado_resumo_e_relatorio_por_tipo_erro():
    linhas = [{"valor": "1"}, {"valor": "3"}, {"outra": "x"}]

    resultado = _pipeline(linhas).executar()

    assert "1 registro(s) importado(s) com sucesso" in resultado.resumo()
    assert "2 falha(s)" in resultado.resumo()
    assert resultado.relatorio_por_tipo_erro() == {"ValueError": 1, "KeyError": 1}


def test_exportar_falhas_csv_grava_dados_originais_e_diagnostico(tmp_path):
    linhas = [{"valor": "3"}]
    resultado = _pipeline(linhas).executar()

    caminho = tmp_path / "falhas.csv"
    resultado.exportar_falhas_csv(caminho)

    conteudo = caminho.read_text(encoding="utf-8")
    assert "valor" in conteudo
    assert "ValueError" in conteudo
    assert "numero_linha" in conteudo


def test_exportar_falhas_csv_nao_cria_arquivo_se_nao_houver_falhas(tmp_path):
    linhas = [{"valor": "1"}]
    resultado = _pipeline(linhas).executar()

    caminho = tmp_path / "falhas.csv"
    resultado.exportar_falhas_csv(caminho)

    assert not caminho.exists()


def test_gerenciador_transacao_confirma_a_cada_linha_bem_sucedida():
    gerenciador = GerenciadorDeTransacaoFalso()
    linhas = [{"valor": "1"}, {"valor": "2"}]

    _pipeline(linhas, gerenciador_transacao=gerenciador).executar()

    assert gerenciador.chamadas == ["confirmar", "confirmar"]


def test_gerenciador_transacao_desfaz_so_a_linha_que_falhou():
    gerenciador = GerenciadorDeTransacaoFalso()
    linhas = [{"valor": "1"}, {"valor": "3"}, {"valor": "5"}]

    resultado = _pipeline(linhas, gerenciador_transacao=gerenciador).executar()

    assert gerenciador.chamadas == ["confirmar", "desfazer", "confirmar"]
    assert len(resultado.sucessos) == 2
    assert len(resultado.erros) == 1


def test_sem_gerenciador_transacao_pipeline_funciona_normalmente():
    """O parâmetro é opcional -- todo o comportamento anterior (sem
    ele) continua exatamente igual, é o que os outros testes deste
    arquivo já provam ao não passar gerenciador_transacao nenhum."""
    linhas = [{"valor": "1"}, {"valor": "3"}]

    resultado = _pipeline(linhas, gerenciador_transacao=None).executar()

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
