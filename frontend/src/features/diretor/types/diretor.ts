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