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

/**
 * Realiza uma requisição HTTP de envio de arquivo (multipart/form-data).
 *
 * Não pode reutilizar `requisicao`: aquela função sempre define
 * `Content-Type: application/json`, e um upload multipart precisa
 * que o navegador gere esse cabeçalho sozinho (com o boundary do
 * multipart) — o que só acontece se nenhum Content-Type for
 * definido manualmente na requisição.
 *
 * @param endpoint Caminho do recurso na API.
 * @param dados Dados do formulário, incluindo o arquivo.
 * @returns Dados retornados pela API.
 */
export async function requisicaoArquivo<T>(
  endpoint: string,
  dados: FormData,
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    body: dados,
  });

  if (!response.ok) {
    const corpo = await response.json().catch(() => null);

    throw new Error(
      corpo?.mensagem ??
        `Erro na API: ${response.status} ${response.statusText}`,
    );
  }

  return response.json() as Promise<T>;
}