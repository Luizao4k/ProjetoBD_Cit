import { useState } from "react";
import { AlertCircle, RotateCcw } from "lucide-react";

import {
  type TipoImportacao,
} from "../../features/importacao/types/importacao";

import {
  importarArquivo,
  type ResultadoImportacaoApi,
} from "../../features/importacao/services/importacaoService";
import { baixarFalhasCsv } from "../../features/importacao/utils/falhasCsv";

import { SeletorTipoImportacao } from "../../features/importacao/components/SeletorTipoImportacao";
import { UploadArquivo } from "../../features/importacao/components/UploadArquivo";
import { ResultadoImportacao } from "../../features/importacao/components/ResultadoImportacao";

import "./importacao.css";

type EstadoImportacao =
  | "nova"
  | "processando"
  | "resultado"
  | "erro";

/**
 * Página responsável pela importação de dados.
 */
export function ImportacaoPage() {
  const [tipoImportacao, setTipoImportacao] =
    useState<TipoImportacao>("dre");

  const [arquivo, setArquivo] =
    useState<File | null>(null);

  const [estado, setEstado] =
    useState<EstadoImportacao>("nova");

  const [resultado, setResultado] =
    useState<ResultadoImportacaoApi | null>(null);

  const [mensagemErro, setMensagemErro] =
    useState<string | null>(null);

  async function handleImportar() {
    if (!arquivo) {
      return;
    }

    setEstado("processando");

    try {
      const resposta = await importarArquivo(tipoImportacao, arquivo);

      setResultado(resposta);
      setEstado("resultado");
    } catch (error) {
      console.error("Erro ao importar arquivo:", error);

      setMensagemErro(
        error instanceof Error
          ? error.message
          : "Não foi possível concluir a importação.",
      );
      setEstado("erro");
    }
  }

  function handleNovaImportacao() {
    setArquivo(null);
    setResultado(null);
    setMensagemErro(null);
    setEstado("nova");
  }

  function handleTentarNovamente() {
    setMensagemErro(null);
    setEstado("nova");
  }

  function handleBaixarFalhas() {
    if (!resultado) {
      return;
    }

    baixarFalhasCsv(resultado);
  }

  function renderNovaImportacao() {
    return (
      <div className="importacao-card">
        <div className="importacao-card__header">
          <h2>Nova importação</h2>

          <p>
            Selecione o tipo de dado e o arquivo que deseja
            importar.
          </p>
        </div>

        <div className="importacao-card__body">
          <SeletorTipoImportacao
            valor={tipoImportacao}
            onChange={setTipoImportacao}
          />

          <UploadArquivo
            arquivo={arquivo}
            onChange={setArquivo}
          />
        </div>

        <footer className="importacao-card__footer">
          <button
            type="button"
            className="importacao-button"
            onClick={handleImportar}
            disabled={!arquivo}
          >
            Importar arquivo
          </button>
        </footer>
      </div>
    );
  }

  function renderProcessando() {
    return (
      <div className="importacao-card importacao-processando">
        <div className="importacao-processando__content">
          <div className="importacao-processando__spinner" />

          <h2>Processando importação</h2>

          <p>
            O arquivo está sendo processado.
          </p>

          <span>
            {arquivo?.name}
          </span>
        </div>
      </div>
    );
  }

  function renderErro() {
    return (
      <div className="importacao-card importacao-erro">
        <div className="importacao-erro__content">
          <div className="importacao-erro__icon">
            <AlertCircle size={26} />
          </div>

          <h2>Não foi possível importar</h2>

          <p>
            {mensagemErro ?? "Ocorreu um erro inesperado durante a importação."}
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

  function renderResultado() {
    if (!resultado) {
      return null;
    }

    return (
      <ResultadoImportacao
        sucessos={resultado.sucessos}
        erros={resultado.erros}
        taxaSucesso={resultado.taxa_sucesso * 100}
        resumo={resultado.resumo}
        onBaixarFalhas={handleBaixarFalhas}
        onNovaImportacao={handleNovaImportacao}
      />
    );
  }

  return (
    <main className="importacao-page">
      <header className="importacao-page__header">
        <div>
          <h1>Importação</h1>

          <p>
            Importe dados do sistema através de arquivos CSV.
          </p>
        </div>
      </header>

      <section className="importacao-page__content">
        {estado === "nova" && renderNovaImportacao()}

        {estado === "processando" && renderProcessando()}

        {estado === "erro" && renderErro()}

        {estado === "resultado" && renderResultado()}
      </section>
    </main>
  );
}
