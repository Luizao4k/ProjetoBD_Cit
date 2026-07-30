"""
Representação rica de uma falha de importação por linha.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class ErroImportacao:
    """
    Tudo que alguém precisa pra entender e corrigir UMA linha que
    falhou, sem reabrir o código:

    - numero_linha: posição no arquivo de origem (1-based, exclui
      cabeçalho), para localizar rapidamente na planilha.
    - dados_originais: a linha crua exatamente como veio do Reader —
      é o que volta gravado no CSV de falhas para reimportação.
    - tipo_erro: nome da classe da exceção (ex: "InepJaCadastradoError",
      "NomeInvalidoError", "KeyError") — machine-readable, dá pra
      agrupar/filtrar falhas por tipo num relatório.
    - mensagem: str(exceção) — a explicação legível por humano.
    - campo: qual coluna originou o problema, quando dá pra saber.
      Best-effort: nem toda exceção de domínio expõe isso hoje: só é
      preenchido se a exceção tiver um atributo `campo`.
    - ocorrido_em: timestamp de quando a falha aconteceu, útil se o
      relatório for reaproveitado como log de auditoria da importação.
    """

    numero_linha: int
    dados_originais: dict[str, str]
    tipo_erro: str
    mensagem: str
    campo: str | None = None
    ocorrido_em: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def a_partir_de(
        cls,
        numero_linha: int,
        dados_originais: dict[str, str],
        excecao: Exception,
    ) -> "ErroImportacao":
        """
        Constrói o erro a partir da exceção capturada pelo Pipeline.
        Funciona para QUALQUER exceção — KeyError de coluna faltante,
        erro de Value Object, erro de persistência — sem precisar de
        um `except` dedicado por tipo.
        """
        return cls(
            numero_linha=numero_linha,
            dados_originais=dict(dados_originais),
            tipo_erro=type(excecao).__name__,
            mensagem=str(excecao),
            campo=getattr(excecao, "campo", None),
        )

    def linha_relatorio(self) -> dict[str, str]:
        """Achata este erro numa linha de dict, pronta para
        csv.DictWriter — dados originais + colunas de diagnóstico."""
        return {
            **{k: str(v) for k, v in self.dados_originais.items()},
            "numero_linha": str(self.numero_linha),
            "tipo_erro": self.tipo_erro,
            "motivo": self.mensagem,
        }
