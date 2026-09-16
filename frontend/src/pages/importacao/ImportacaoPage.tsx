import { useState } from "react";

import {
  type TipoImportacao,
} from "../../features/importacao/types/importacao";

import { SeletorTipoImportacao } from "../../features/importacao/components/SeletorTipoImportacao";
import { UploadArquivo } from "../../features/importacao/components/UploadArquivo";
import { ResultadoImportacao } from "../../features/importacao/components/ResultadoImportacao";

import "./importacao.css";

type EstadoImportacao =
  | "nova"
  | "processando"
  | "resultado";

interface Resultado {
  sucessos: number;
  erros: number;
  taxaSucesso: number;
  resumo: string;
}

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
    useState<Resultado | null>(null);

  function handleImportar() {
    if (!arquivo) {
      return;
    }

    /*
     * Por enquanto, apenas mudamos o estado da interface.
     *
     * A chamada real para a API será adicionada posteriormente.
     */
    setEstado("processando");

    console.log("Tipo:", tipoImportacao);
    console.log("Arquivo:", arquivo);

    /*
     * Temporariamente deixamos o estado de processamento
     * aqui para visualizar a interface.
     *
     * NÃO estamos simulando um resultado.
     */
  }

  function handleNovaImportacao() {
    setArquivo(null);
    setResultado(null);
    setEstado("nova");
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

  function renderResultado() {
    if (!resultado) {
      return null;
    }

    return (
      <ResultadoImportacao
        sucessos={resultado.sucessos}
        erros={resultado.erros}
        taxaSucesso={resultado.taxaSucesso}
        resumo={resultado.resumo}
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

        {estado === "resultado" && renderResultado()}
      </section>
    </main>
  );
}
