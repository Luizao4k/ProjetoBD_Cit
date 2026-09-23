import { useState } from "react";

import {
  type TipoImportacao,
} from "../../features/importacao/types/importacao";

import {
  importarArquivo,
  importarFormulario,
  type ResultadoImportacaoApi,
} from "../../features/importacao/services/importacaoService";

import { baixarFalhasCsv } from "../../features/importacao/utils/falhasCsv";

import { TelaNovaImportacao } from "../../features/importacao/components/TelaNovaImportacao";
import { TelaProcessando } from "../../features/importacao/components/TelaProcessando";
import { TelaErro } from "../../features/importacao/components/TelaErro";
import { TelaResultado } from "../../features/importacao/components/TelaResultado";

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
      <TelaNovaImportacao
        tipoImportacao={tipoImportacao}
        modoImportacao={modoImportacao}
        arquivo={arquivo}
        onTipoImportacaoChange={setTipoImportacao}
        onModoImportacaoChange={setModoImportacao}
        onArquivoChange={setArquivo}
        onImportarFormulario={handleImportarFormulario}
        onImportarArquivo={handleImportarArquivo}
      />
    );
  }

  /**
   * Renderiza o estado de processamento.
   */
  function renderProcessando() {
    return <TelaProcessando />;
  }

  /**
   * Renderiza a tela apresentada quando ocorre um erro.
   */
  function renderErro() {
    return (
      <TelaErro
        mensagem={
          mensagemErro ??
          "Não foi possível concluir a importação."
        }
        onTentarNovamente={handleTentarNovamente}
      />
    );
  }

  /**
   * Renderiza a tela com o resultado da importação.
   */
  function renderResultado() {
    if (!resultado) {
      return null;
    }

    return (
      <TelaResultado
        resultado={resultado}
        onBaixarFalhas={handleBaixarFalhas}
      />
    );
  }

  return (
    <div className="importacao-page">
      {estado === "nova" && renderNovaImportacao()}

      {estado === "processando" && renderProcessando()}

      {estado === "resultado" && renderResultado()}

      {estado === "erro" && renderErro()}
    </div>
  );
}