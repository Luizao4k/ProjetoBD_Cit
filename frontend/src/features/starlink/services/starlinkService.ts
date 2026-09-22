import { requisicao } from "../../../services/http";
import type { Starlink } from "../types/starlink";


export function listarStarlinks(): Promise<Starlink[]> {
  return requisicao<Starlink[]>("/starlinks");
}

export function buscarStarlink(id: number): Promise<Starlink> {
  return requisicao<Starlink>(`/starlinks/${id}`);
}

export function criarStarlink(dados: {
  escola_id: number;
  designacao: string;
}): Promise<Starlink> {
  return requisicao<Starlink>("/starlinks", {
    method: "POST",
    body: JSON.stringify(dados),
  });
}

export function atualizarStarlink(
  id: number,
  dados: {
    designacao?: string;
  },
): Promise<Starlink> {
  return requisicao<Starlink>(`/starlinks/${id}`, {
    method: "PUT",
    body: JSON.stringify(dados),
  });
}

export async function excluirStarlink(id: number): Promise<void> {
  await requisicao<void>(`/starlinks/${id}`, {
    method: "DELETE",
  });
}