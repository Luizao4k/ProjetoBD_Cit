import { requisicao } from "../../../services/http";
import type { Diretor } from "../types/diretor";

/**
 * Retorna todos os diretores cadastrados.
 *
 * @returns Lista de diretores.
 */
export function listarDiretores(): Promise<Diretor[]> {
  return requisicao<Diretor[]>("/diretores");
}

/**
 * Busca um diretor pelo identificador.
 *
 * @param id Identificador do diretor.
 * @returns Diretor encontrado.
 */
export function buscarDiretor(
  id: number,
): Promise<Diretor> {
  return requisicao<Diretor>(`/diretores/${id}`);
}

/**
 * Atualiza os dados editáveis de um diretor.
 */
export function atualizarDiretor(
  id: number,
  dados: {
    nome?: string;
    telefone?: string;
    email?: string;
  },
): Promise<Diretor> {
  return requisicao<Diretor>(`/diretores/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}
