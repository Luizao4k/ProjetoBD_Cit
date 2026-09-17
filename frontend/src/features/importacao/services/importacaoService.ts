import { requisicaoArquivo } from "../../../services/http";
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
 * Espelha ResultadoImportacao no backend
 * (infrastructure/importacao/resultado.py). `taxa_sucesso` vem como
 * fração entre 0 e 1 — quem exibe é responsável por converter para
 * percentual.
 */
export interface ResultadoImportacaoApi {
  tipo: TipoImportacao;
  arquivo: string;
  total_processado: number;
  sucessos: number;
  erros: number;
  taxa_sucesso: number;
  resumo: string;
  falhas: FalhaImportacao[];
}

/**
 * Envia um arquivo (CSV ou Excel) para importação em lote de um dos
 * tipos de dado suportados pelo sistema.
 *
 * Cada linha inválida do arquivo não interrompe a importação — ela
 * aparece em `falhas`, dentro de um resultado 200. A Promise só
 * rejeita quando a requisição em si falha (tipo inválido, arquivo
 * ausente, arquivo estruturalmente inválido, erro de rede).
 */
export function importarArquivo(
  tipo: TipoImportacao,
  arquivo: File,
): Promise<ResultadoImportacaoApi> {
  const dados = new FormData();
  dados.append("tipo", tipo);
  dados.append("arquivo", arquivo);

  return requisicaoArquivo<ResultadoImportacaoApi>("/importacao", dados);
}
