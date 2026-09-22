/**
 * Representa uma starlink retornada pela API.
 */
export interface Starlink {
/** Identificador único da starlink. */
  id: number;
/** Identificador único da escola vinculada */
  escola_id: number;
/** Codigo da designação starlink*/
  designacao: string;
/** Data e hora de criação do registro. */
  criado_em: string;
/** Data e hora da última atualização do registro. */
  atualizado_em: string;
}