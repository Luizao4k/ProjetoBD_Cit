"""
Resolvedores de chave estrangeira compartilhados por mais de um
Mapper — extraídos aqui pra não duplicar a mesma lógica de resolução
em 4 arquivos diferentes. Cada um aceita o id direto OU um
identificador amigável, e busca no repositório correspondente.

A resolução de dre_id (dre_id ou dre_nome) mora dentro do próprio
EscolaMapper porque só tem um consumidor.
"""

from __future__ import annotations

from backend.domain.repositories import CemepRepository, EscolaRepository
from backend.domain.value_objects import Inep


def resolver_escola_id(linha: dict[str, str], repo_escola: EscolaRepository) -> int:
    """
    Usado por DiretorMapper, CemepMapper, ChromebookMapper e
    StarlinkMapper — todos precisam do mesmo escola_id.

    Diferente da resolução de DRE por nome (em EscolaMapper), aqui
    não existe caso de ambiguidade: inep é UNIQUE no schema de
    escolas, então buscar_por_inep devolve no máximo uma Escola.
    """
    escola_id_bruto = (linha.get("escola_id") or "").strip()
    if escola_id_bruto:
        return int(escola_id_bruto)

    inep = (linha.get("escola_inep") or "").strip()
    if not inep:
        raise ValueError("Linha não informou nem escola_id nem escola_inep.")

    escola = repo_escola.buscar_por_inep(Inep(inep))
    if escola is None:
        raise ValueError(f"Escola com INEP '{inep}' não encontrada.")
    if escola.id is None:
        # Defensivo, não cosmético: escola.id é Optional no domínio
        # (uma Escola ainda não salva não tem id), mas uma que veio de
        # buscar_por_inep já está persistida — se isso disparar, é bug
        # de outra camada, não uma linha de CSV mal formatada.
        raise ValueError(f"Escola com INEP '{inep}' não possui id persistido.")

    return escola.id


def resolver_cemep_id(
    linha: dict[str, str],
    repo_cemep: CemepRepository,
    repo_escola: EscolaRepository,
) -> int:
    """
    Usado por ResponsavelMapper. Cemep não tem nome próprio — só
    existe em função da escola a que pertence (relação 1:1) —, então
    o único identificador amigável possível é o escola_inep da escola
    à qual o CEMEP pertence.
    """
    cemep_id_bruto = (linha.get("cemep_id") or "").strip()
    if cemep_id_bruto:
        return int(cemep_id_bruto)

    inep = (linha.get("escola_inep") or "").strip()
    if not inep:
        raise ValueError("Linha não informou nem cemep_id nem escola_inep.")

    escola = repo_escola.buscar_por_inep(Inep(inep))
    if escola is None:
        raise ValueError(f"Escola com INEP '{inep}' não encontrada.")
    if escola.id is None:
        raise ValueError(f"Escola com INEP '{inep}' não possui id persistido.")

    cemep = repo_cemep.buscar_por_escola(escola.id)
    if cemep is None:
        raise ValueError(f"Escola com INEP '{inep}' não possui CEMEP cadastrado.")
    if cemep.id is None:
        raise ValueError(f"CEMEP da escola com INEP '{inep}' não possui id persistido.")

    return cemep.id
