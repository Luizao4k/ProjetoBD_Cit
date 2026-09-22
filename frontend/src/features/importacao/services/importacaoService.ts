import { requisicao, requisicaoArquivo } from "../../../services/http";

import type { TipoImportacao } from "../types/importacao";

/**
 * Uma linha do arquivo que não pôde ser importada.
 *
 * Espelha ErroImportacao no backend
 * (infrastructure/importacao/erro.py).
 */
export interface FalhaImportacao {
  numero_linha: number;
  tipo_erro: string;
  mensagem: string;
  campo: string | null;
  dados_originais: Record<string, string>;
  ocorrido_em: string;
}

/**
 * Relatório de uma importação retornado pela API.
 *
 * Espelha ResultadoImportacao no backend.
 */
export interface ResultadoImportacaoApi {
  tipo: TipoImportacao;
  arquivo: string | null;
  total_processado: number;
  sucessos: number;
  erros: number;
  taxa_sucesso: number;
  resumo: string;
  falhas: FalhaImportacao[];
}

/**
 * Envia um arquivo CSV ou Excel para importação em lote.
 */
export function importarArquivo(
  tipo: TipoImportacao,
  arquivo: File,
): Promise<ResultadoImportacaoApi> {
  const dados = new FormData();

  dados.append("tipo", tipo);
  dados.append("arquivo", arquivo);

  return requisicaoArquivo<ResultadoImportacaoApi>(
    "/importacao",
    dados,
  );
}

/**
 * Dados fornecidos diretamente por um formulário.
 *
 * Os campos são enviados como valores simples para a API.
 */
export type DadosFormularioImportacao = Record<string, string>;

/**
 * Envia dados preenchidos em formulário para o mesmo fluxo
 * de importação utilizado pelos arquivos.
 */
export function importarFormulario(
  tipo: TipoImportacao,
  dados: DadosFormularioImportacao,
): Promise<ResultadoImportacaoApi> {
  return requisicao<ResultadoImportacaoApi>("/importacao/formulario", {
    method: "POST",
    body: JSON.stringify({
      tipo,
      dados,
    }),
  });
}