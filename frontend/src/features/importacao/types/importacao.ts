/**
 * Tipos de dados que podem ser importados pelo sistema.
 */
export type TipoImportacao =
  | "dre"
  | "escolas"
  | "diretores"
  | "cemeps"
  | "chromebooks"
  | "starlinks"
  | "responsaveis"
  | "turmas_cemep";

/**
 * Representa uma opção disponível na interface de importação.
 */
export interface OpcaoImportacao {
  tipo: TipoImportacao;
  nome: string;
}