const API_URL = "http://localhost:5000";

export interface Dre {
  id: number;
  nome: string;
  telefone: string | null;
  criado_em: string;
  atualizado_em: string;
}

async function requisicao<T>(
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

export function listarDres(): Promise<Dre[]> {
  return requisicao<Dre[]>("/dres");
}

export async function buscarDre(id: number): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`);
}

export async function criarDre(dados: {
  nome: string;
  telefone?: string;
}): Promise<Dre> {
  return requisicao<Dre>("/dres", {
    method: "POST",
    body: JSON.stringify(dados),
  });
}

export async function atualizarDre(
  id: number,
  dados: {
    nome?: string;
    telefone?: string;
  },
): Promise<Dre> {
  return requisicao<Dre>(`/dres/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}

export async function excluirDre(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/dres/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(
      `Erro na API: ${response.status} ${response.statusText}`,
    );
  }
}