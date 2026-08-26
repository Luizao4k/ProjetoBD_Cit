import { requisicao } from "./http";

/**
 * Representa uma DRE retornada pela API.
 */
export interface Dre {
  /** Identificador único da DRE. */
  id: number;

  /** Nome da DRE. */
  nome: string;

  /** Telefone de contato, quando informado. */
  telefone: string | null;

  /** Data e hora de criação do registro. */
  criado_em: string;

  /** Data e hora da última atualização do registro. */
  atualizado_em: string;
}

/**
 * Retorna todas as DREs cadastradas.
 *
 * @returns Lista de DREs.
 */
export function listarDres(): Promise<Dre[]> {
  return requisicao<Dre[]>("/dres");
}

/**
 * Busca uma DRE pelo seu identificador.
 *
 * @param id Identificador da DRE.
 * @returns DRE encontrada.
 */
export function buscarDre(id: number): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`);
}

/**
 * Cria uma nova DRE.
 *
 * @param dados Dados necessários para criação da DRE.
 * @returns DRE criada.
 */
export function criarDre(dados: {
  nome: string;
  telefone?: string;
}): Promise<Dre> {
  return requisicao<Dre>("/dres", {
    method: "POST",
    body: JSON.stringify(dados),
  });
}

/**
 * Atualiza uma DRE existente.
 *
 * @param id Identificador da DRE.
 * @param dados Campos que serão atualizados.
 * @returns DRE atualizada.
 */
export function atualizarDre(
  id: number,
  dados: {
    nome?: string;
    telefone?: string;
  },
): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}

/**
 * Remove uma DRE.
 *
 * @param id Identificador da DRE.
 */
export async function excluirDre(id: number): Promise<void> {
  await requisicao<void>(`/dres/${id}`, {
    method: "DELETE",
  });
}