/**
 * Formata uma string de números para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.
 * Trata valores nulos ou indefinidos de forma segura.
 */
export const formatarTelefone = (telefone: string | null | undefined): string => {
  if (!telefone) return '';

  const apenasNumeros = telefone.replace(/\D/g, '');

  if (apenasNumeros.length === 11) {
    return apenasNumeros.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
  } else if (apenasNumeros.length === 10) {
    return apenasNumeros.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
  }

  return telefone; // Retorna o texto original caso não bata com as regras
};
