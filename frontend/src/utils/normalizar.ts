/**
 * Normaliza um texto para comparação.
 *
 * Remove acentos, converte para minúsculas
 * e remove espaços nas extremidades.
 */
export function normalizarTexto(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}