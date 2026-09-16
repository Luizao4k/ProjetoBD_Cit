import type { OpcaoImportacao } from "./importacao";

/**
 * Tipos de importação disponíveis no sistema.
 */
export const OPCOES_IMPORTACAO: OpcaoImportacao[] = [
  {
    tipo: "dre",
    nome: "DREs",
  },
  {
    tipo: "escolas",
    nome: "Escolas",
  },
  {
    tipo: "diretores",
    nome: "Diretores",
  },
  {
    tipo: "cemeps",
    nome: "CEMEPs",
  },
  {
    tipo: "chromebooks",
    nome: "Chromebooks",
  },
  {
    tipo: "starlinks",
    nome: "Starlinks",
  },
  {
    tipo: "responsaveis",
    nome: "Responsáveis",
  },
  {
    tipo: "turmas_cemep",
    nome: "Turmas CEMEP",
  },
];