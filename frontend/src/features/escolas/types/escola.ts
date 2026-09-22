import type { Dre } from "../../dre/types/dre";

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
  /** Informações da DRE responsável pela escola */
  dre?: Dre | null;   

  /** Endereço da escola, quando informado. */
  endereco: string | null;

  /** Data e hora de criação do registro. */
  criado_em: string;

  /** Data e hora da última atualização do registro. */
  atualizado_em: string;
}