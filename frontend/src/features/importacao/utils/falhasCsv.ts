import type {
  FalhaImportacao,
  ResultadoImportacaoApi,
} from "../services/importacaoService";

/**
 * Escapa um valor para uma célula CSV (RFC 4180): entre aspas
 * quando o valor contém vírgula, aspas ou quebra de linha; aspas
 * internas são duplicadas.
 */
function escaparCampoCsv(valor: string): string {
  if (/[",\r\n]/.test(valor)) {
    return `"${valor.replace(/"/g, '""')}"`;
  }

  return valor;
}

/**
 * Monta um CSV com as linhas que falharam numa importação — mesmo
 * formato do relatório gerado pelos scripts de CLI (ver
 * ResultadoImportacao.exportar_falhas_csv no backend): colunas
 * originais do arquivo enviado, seguidas de numero_linha, tipo_erro
 * e motivo. Pensado para abrir numa planilha, corrigir os dados e
 * reimportar como um novo arquivo.
 */
function montarCsvFalhas(falhas: FalhaImportacao[]): string {
  const colunasOriginais = Object.keys(falhas[0].dados_originais);
  const colunas = [...colunasOriginais, "numero_linha", "tipo_erro", "motivo"];

  const linhas = falhas.map((falha) => {
    const valores: Record<string, string> = {
      ...falha.dados_originais,
      numero_linha: String(falha.numero_linha),
      tipo_erro: falha.tipo_erro,
      motivo: falha.mensagem,
    };

    return colunas
      .map((coluna) => escaparCampoCsv(valores[coluna] ?? ""))
      .join(",");
  });

  return [colunas.join(","), ...linhas].join("\r\n");
}

/**
 * Gera o CSV de falhas de uma importação e inicia o download no
 * navegador. Não faz nenhuma requisição à API — usa só os dados já
 * devolvidos por `importarArquivo`.
 */
export function baixarFalhasCsv(resultado: ResultadoImportacaoApi): void {
  if (resultado.falhas.length === 0) {
    return;
  }

  const conteudo = montarCsvFalhas(resultado.falhas);

  // O BOM (\uFEFF) no início faz o Excel reconhecer UTF-8
  // automaticamente — sem ele, nomes e municípios com acento
  // aparecem corrompidos ao abrir o CSV no Windows.
  const blob = new Blob(["\uFEFF" + conteudo], {
    type: "text/csv;charset=utf-8;",
  });

  const nomeBase = resultado.arquivo.replace(/\.[^./]+$/, "");
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = `${nomeBase}_falhas.csv`;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}
