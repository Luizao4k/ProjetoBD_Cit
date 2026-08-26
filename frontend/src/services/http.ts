const API_URL = "http://localhost:5000";

/**
 * Realiza uma requisição HTTP para a API.
 *
 * Esta função centraliza a comunicação HTTP do frontend,
 * deixando os serviços específicos responsáveis apenas
 * pelas operações relacionadas aos seus respectivos recursos.
 *
 * @param endpoint Caminho do recurso na API.
 * @param options Opções adicionais da requisição HTTP.
 * @returns Dados retornados pela API.
 */
export async function requisicao<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erro na API: ${response.status} ${response.statusText}`,
    );
  }

  return response.json() as Promise<T>;
}