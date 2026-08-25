"""
Testes de interface.serializacao.dto_para_dict.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from apresentation.serializacao import dto_para_dict


@dataclass
class _DtoDeTeste:
    id: int
    nome: str
    criado_em: datetime


def test_converte_datetime_para_string_iso():
    dto = _DtoDeTeste(id=1, nome="Teste", criado_em=datetime(2026, 1, 15, 10, 30))

    resultado = dto_para_dict(dto)

    assert resultado["criado_em"] == "2026-01-15T10:30:00"
    assert resultado["id"] == 1
    assert resultado["nome"] == "Teste"


def test_campos_none_permanecem_none():
    @dataclass
    class _ComOpcional:
        telefone: str | None

    resultado = dto_para_dict(_ComOpcional(telefone=None))

    assert resultado["telefone"] is None


def test_funciona_com_dto_real_de_dre():
    from application.use_cases.dre import DreOutput

    saida = DreOutput(
        id=1,
        nome="DRE BELEM",
        telefone=None,
        criado_em=datetime(2026, 1, 1),
        atualizado_em=datetime(2026, 1, 1),
    )

    resultado = dto_para_dict(saida)

    assert resultado == {
        "id": 1,
        "nome": "DRE BELEM",
        "telefone": None,
        "criado_em": "2026-01-01T00:00:00",
        "atualizado_em": "2026-01-01T00:00:00",
    }
