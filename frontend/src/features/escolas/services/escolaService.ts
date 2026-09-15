import { requisicao } from "../../../services/http";

/**
 * Representa uma escola retornada pela API.
 */
export interface Escola {
  /** Identificador único da escola. */
  id: number;

  /** Código INEP da escola. */
  inep: string;

  /** Nome da escola. */
  nome: string;

  /** Tipo da escola. */
  tipo: string;

  /** Município onde a escola está localizada. */
  municipio: string;

  /** Identificador da DRE responsável pela escola. */
  dre_id: number;

  /** Endereço da escola, quando informado. */
  endereco: string | null;

  /** Data e hora de criação do registro. */
  criado_em: string;

  /** Data e hora da última atualização do registro. */
  atualizado_em: string;
}

/**
 * Retorna todas as escolas cadastradas.
 *
 * @returns Lista de escolas.
 */
export function listarEscolas(): Promise<Escola[]> {
  return requisicao<Escola[]>("/escolas");
}

/**
 * Busca uma escola pelo seu identificador.
 *
 * @param id Identificador da escola.
 * @returns Escola encontrada.
 */
export function buscarEscola(id: number): Promise<Escola> {
  return requisicao<Escola>(`/escolas/${id}`);
}

/**
 * Cria uma nova escola.
 *
 * @param dados Dados necessários para criação da escola.
 * @returns Escola criada.
 */
export function criarEscola(dados: {
  inep: string;
  nome: string;
  tipo: string;
  municipio: string;
  dre_id: number;
  endereco?: string;
}): Promise<Escola> {
  return requisicao<Escola>("/escolas", {
    method: "POST",
    body: JSON.stringify(dados),
  });
}

/**
 * Atualiza os dados editáveis de uma escola.
 *
 * INEP, tipo e município são imutáveis no domínio.
 *
 * @param id Identificador da escola.
 * @param dados Dados que serão alterados.
 * @returns Escola atualizada.
 */
export function atualizarEscola(
  id: number,
  dados: {
    nome?: string;
    endereco?: string;
  },
): Promise<Escola> {
  return requisicao<Escola>(`/escolas/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}

/**
 * Remove uma escola pelo seu identificador.
 *
 * @param id Identificador da escola.
 */
export async function excluirEscola(id: number): Promise<void> {
  await requisicao<void>(`/escolas/${id}`, {
    method: "DELETE",
  });
}
