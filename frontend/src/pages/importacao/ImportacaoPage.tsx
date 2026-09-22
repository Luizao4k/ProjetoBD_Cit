import { useState } from "react";

import { AlertCircle, RotateCcw } from "lucide-react";

import {
  type TipoImportacao,
} from "../../features/importacao/types/importacao";

import {
  importarArquivo,
  importarFormulario,
  type ResultadoImportacaoApi,
} from "../../features/importacao/services/importacaoService";

import { baixarFalhasCsv } from "../../features/importacao/utils/falhasCsv";

import { SeletorTipoImportacao } from "../../features/importacao/components/SeletorTipoImportacao";

import { UploadArquivo } from "../../features/importacao/components/UploadArquivo";

import { ResultadoImportacao } from "../../features/importacao/components/ResultadoImportacao";

import { FormularioImportacao } from "../../features/importacao/components/FormularioImportacao";

import "./importacao.css";

type EstadoImportacao =
  | "nova"
  | "processando"
  | "resultado"
  | "erro";

type ModoImportacao =
  | "arquivo"
  | "formulario";

/**
 * Página responsável pela importação de dados.
 */
export function ImportacaoPage() {
  const [tipoImportacao, setTipoImportacao] =
    useState<TipoImportacao>("dre");

  const [modoImportacao, setModoImportacao] =
    useState<ModoImportacao>("arquivo");

  const [arquivo, setArquivo] =
    useState<File | null>(null);

  const [estado, setEstado] =
    useState<EstadoImportacao>("nova");

  const [resultado, setResultado] =
    useState<ResultadoImportacaoApi | null>(null);

  const [mensagemErro, setMensagemErro] =
    useState<string | null>(null);

  /**
   * Realiza uma importação através de arquivo.
   */
  async function handleImportarArquivo() {
    if (!arquivo) {
      return;
    }

    setEstado("processando");

    try {
      const resposta = await importarArquivo(
        tipoImportacao,
        arquivo,
      );

      setResultado(resposta);
      setEstado("resultado");
    } catch (error) {
      console.error(
        "Erro ao importar arquivo:",
        error,
      );

      setMensagemErro(
        error instanceof Error
          ? error.message
          : "Não foi possível concluir a importação.",
      );

      setEstado("erro");
    }
  }

  /**
   * Realiza uma importação através de formulário.
   */
  async function handleImportarFormulario(
    dados: Record<string, string>,
  ) {
    setEstado("processando");

    try {
      const resposta = await importarFormulario(
        tipoImportacao,
        dados,
      );

      setResultado(resposta);
      setEstado("resultado");
    } catch (error) {
      console.error(
        "Erro ao importar formulário:",
        error,
      );

      setMensagemErro(
        error instanceof Error
          ? error.message
          : "Não foi possível concluir a importação.",
      );

      setEstado("erro");
    }
  }

  /**
   * Reinicia a página para uma nova importação.
   */
  function handleNovaImportacao() {
    setArquivo(null);
    setResultado(null);
    setMensagemErro(null);
    setModoImportacao("arquivo");
    setEstado("nova");
  }

  /**
   * Retorna para o estado inicial após um erro.
   */
  function handleTentarNovamente() {
    setMensagemErro(null);
    setEstado("nova");
  }

  /**
   * Baixa o relatório das linhas que apresentaram erro.
   */
  function handleBaixarFalhas() {
    if (!resultado) {
      return;
    }

    baixarFalhasCsv(resultado);
  }

  /**
   * Renderiza a tela inicial de importação.
   */
  function renderNovaImportacao() {
    return (
      <div className="importacao-card">
        <div className="importacao-card__header">
          <h2>Nova importação</h2>

          <p>
            Selecione o tipo de dado e a forma de
            entrada.
          </p>
        </div>

        <div className="importacao-card__body">
          <SeletorTipoImportacao
            valor={tipoImportacao}
            onChange={setTipoImportacao}
          />

          <div className="importacao-modo">
            <h3>Forma de entrada</h3>

            <div className="importacao-modo__opcoes">
              
              <button
                type="button"
                className={
                  modoImportacao === "formulario"
                    ? "ativo"
                    : ""
                }
                onClick={() =>
                  setModoImportacao("formulario")
                }
              >
                Formulário
              </button>

              <button
                type="button"
                className={
                  modoImportacao === "arquivo"
                    ? "ativo"
                    : ""
                }
                onClick={() =>
                  setModoImportacao("arquivo")
                }
              >
                Arquivo
              </button>

            </div>
          </div>

          {modoImportacao === "arquivo" && (
            <UploadArquivo
              arquivo={arquivo}
              onChange={setArquivo}
            />
          )}

          {modoImportacao === "formulario" && (
            <FormularioImportacao
              tipo={tipoImportacao}
              onImportar={handleImportarFormulario}
            />
          )}
          
        </div>

        {modoImportacao === "arquivo" && (
          <footer className="importacao-card__footer">
            <button
              type="button"
              className="importacao-button"
              onClick={handleImportarArquivo}
              disabled={!arquivo}
            >
              Importar arquivo
            </button>
          </footer>
        )}
      </div>
    );
  }

  /**
   * Renderiza o estado de processamento.
   */
  function renderProcessando() {
    return (
      <div className="importacao-card importacao-processando">
        <div className="importacao-processando__content">
          <div className="importacao-processando__spinner" />

          <h2>
            Processando importação
          </h2>

          <p>
            Os dados estão sendo processados.
          </p>

          {modoImportacao === "arquivo" &&
            arquivo && (
              <span>
                {arquivo.name}
              </span>
            )}
        </div>
      </div>
    );
  }

  /**
   * Renderiza o estado de erro.
   */
  function renderErro() {
    return (
      <div className="importacao-card importacao-erro">
        <div className="importacao-erro__content">
          <div className="importacao-erro__icon">
            <AlertCircle size={26} />
          </div>

          <h2>
            Não foi possível importar
          </h2>

          <p>
            {mensagemErro ??
              "Ocorreu um erro inesperado durante a importação."}
          </p>

          <button
            type="button"
            className="importacao-erro__retry"
            onClick={handleTentarNovamente}
          >
            <RotateCcw size={17} />
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  /**
   * Renderiza o resultado da importação.
   */
  function renderResultado() {
    if (!resultado) {
      return null;
    }

    return (
      <ResultadoImportacao
        sucessos={resultado.sucessos}
        erros={resultado.erros}
        taxaSucesso={
          resultado.taxa_sucesso * 100
        }
        resumo={resultado.resumo}
        onBaixarFalhas={
          handleBaixarFalhas
        }
        onNovaImportacao={
          handleNovaImportacao
        }
      />
    );
  }

  return (
    <main className="importacao-page">
      <header className="importacao-page__header">
        <div>
          <h1>Importação</h1>

          <p>
            Adicione dados ao sistema através de
            arquivos ou formulários.
          </p>
        </div>
      </header>

      <section className="importacao-page__content">
        {estado === "nova" &&
          renderNovaImportacao()}

        {estado === "processando" &&
          renderProcessando()}

        {estado === "erro" &&
          renderErro()}

        {estado === "resultado" &&
          renderResultado()}
      </section>
    </main>
  );
}
