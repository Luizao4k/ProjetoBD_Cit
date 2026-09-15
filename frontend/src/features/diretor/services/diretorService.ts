import { requisicao } from "../../../services/http";

/**
 * Representa um diretor retornado pela API.
 */
export interface Diretor {
  /**
   * Identificador único do diretor.
   */
  id: number;

  /**
   * Identificador da escola vinculada ao diretor.
   */
  escola_id: number;

  /**
   * Nome do diretor.
   */
  nome: string;

  /**
   * Telefone do diretor, quando informado.
   */
  telefone: string | null;

  /**
   * E-mail do diretor, quando informado.
   */
  email: string | null;

  /**
   * Data e hora de criação do registro.
   */
  criado_em: string;

  /**
   * Data e hora da última atualização do registro.
   */
  atualizado_em: string;
}

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
