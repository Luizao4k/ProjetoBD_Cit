"""
Serialização de DTOs (dataclasses da camada de aplicação) para dict
JSON-seguro.
"""

from __future__ import annotations

import dataclasses
from datetime import date, datetime
from typing import Any


def dto_para_dict(dto: Any) -> dict[str, Any]:
    """
    Converte um DTO (dataclass) num dict pronto para `jsonify`.

    Existe porque `json.dumps` não serializa `datetime` sozinho, e os
    Output DTOs da camada de aplicação (ex: DreOutput, EscolaOutput)
    têm `criado_em`/`atualizado_em: datetime`. Genérico o bastante
    para qualquer DTO atual ou futuro — não precisa de uma versão por
    entidade.
    """
    return _normalizar(dataclasses.asdict(dto))


def _normalizar(valor: Any) -> Any:
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {chave: _normalizar(v) for chave, v in valor.items()}
    if isinstance(valor, list):
        return [_normalizar(v) for v in valor]
    return valor
