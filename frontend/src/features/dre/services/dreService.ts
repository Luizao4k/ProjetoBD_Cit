import { requisicao } from "../../../services/http";
import type { Dre } from "../types/dre";
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