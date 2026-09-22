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
