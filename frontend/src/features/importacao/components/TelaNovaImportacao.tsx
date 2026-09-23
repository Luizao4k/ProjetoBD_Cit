import type { TipoImportacao } from "../types/importacao";

import { SeletorTipoImportacao } from "./SeletorTipoImportacao";
import { UploadArquivo } from "./UploadArquivo";
import { FormularioImportacao } from "./FormularioImportacao";

/**
 * Modos disponíveis para entrada dos dados.
 *
 * - arquivo: importação através de arquivo;
 * - formulario: preenchimento manual através de formulário.
 */
type ModoImportacao = "arquivo" | "formulario";

/**
 * Propriedades utilizadas pelo componente TelaNovaImportacao.
 */
interface TelaNovaImportacaoProps {
  /**
   * Tipo de dado que será importado.
   */
  tipoImportacao: TipoImportacao;

  /**
   * Forma utilizada para fornecer os dados da importação.
   */
  modoImportacao: ModoImportacao;

  /**
   * Arquivo atualmente selecionado para importação.
   *
   * Quando nenhum arquivo foi selecionado, o valor é null.
   */
  arquivo: File | null;

  /**
   * Atualiza o tipo de importação selecionado.
   */
  onTipoImportacaoChange: (tipo: TipoImportacao) => void;

  /**
   * Atualiza o modo de importação selecionado.
   */
  onModoImportacaoChange: (modo: ModoImportacao) => void;

  /**
   * Atualiza o arquivo selecionado pelo usuário.
   */
  onArquivoChange: (arquivo: File | null) => void;

  /**
   * Executa a importação através de formulário.
   *
   * A página permanece responsável pela comunicação
   * com o serviço de importação.
   */
  onImportarFormulario: (
    dados: Record<string, string>,
  ) => Promise<void>;

  /**
   * Executa a importação do arquivo selecionado.
   */
  onImportarArquivo: () => void;
}

/**
 * Apresenta a tela inicial para criação de uma nova importação.
 *
 * Responsabilidades:
 * - permitir a escolha do tipo de dado;
 * - permitir a escolha da forma de entrada;
 * - apresentar o componente de upload quando o modo for arquivo;
 * - apresentar o formulário quando o modo for formulário;
 * - solicitar à página a execução da importação.
 *
 * Este componente não realiza chamadas à API.
 */
export function TelaNovaImportacao({
  tipoImportacao,
  modoImportacao,
  arquivo,
  onTipoImportacaoChange,
  onModoImportacaoChange,
  onArquivoChange,
  onImportarFormulario,
  onImportarArquivo,
}: TelaNovaImportacaoProps) {
  return (
    <div className="importacao-card">
      <div className="importacao-card__header">
        <h2>Nova importação</h2>

        <p>
          Selecione o tipo de dado e a forma de entrada.
        </p>
      </div>

      <div className="importacao-card__body">
        <SeletorTipoImportacao
          valor={tipoImportacao}
          onChange={onTipoImportacaoChange}
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
                onModoImportacaoChange("formulario")
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
                onModoImportacaoChange("arquivo")
              }
            >
              Arquivo
            </button>
          </div>
        </div>

        {modoImportacao === "arquivo" && (
          <UploadArquivo
            arquivo={arquivo}
            onChange={onArquivoChange}
          />
        )}

        {modoImportacao === "formulario" && (
          <FormularioImportacao
            tipo={tipoImportacao}
            onImportar={onImportarFormulario}
          />
        )}
      </div>

      {modoImportacao === "arquivo" && (
        <footer className="importacao-card__footer">
          <button
            type="button"
            className="importacao-button"
            onClick={onImportarArquivo}
            disabled={!arquivo}
          >
            Importar arquivo
          </button>
        </footer>
      )}
    </div>
  );
}