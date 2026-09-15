import { requisicao } from "../../../services/http";

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
 * Dados permitidos para atualização de uma DRE.
 *
 * Todos os campos são opcionais porque a API permite
 * atualização parcial do registro.
 */
export interface AtualizarDreDados {
  nome?: string;
  telefone?: string;
}

/**
 * Retorna todas as DREs cadastradas.
 */
export function listarDres(): Promise<Dre[]> {
  return requisicao<Dre[]>("/dres");
}

/**
 * Busca uma DRE pelo seu identificador.
 */
export function buscarDre(id: number): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`);
}

/**
 * Cria uma nova DRE.
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
 * A atualização é parcial. Somente os campos informados
 * serão enviados para a API.
 */
export function atualizarDre(
  id: number,
  dados: AtualizarDreDados,
): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}

/**
 * Remove uma DRE.
 */
export async function excluirDre(id: number): Promise<void> {
  await requisicao<void>(`/dres/${id}`, {
    method: "DELETE",
  });
}