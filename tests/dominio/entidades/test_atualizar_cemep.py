from datetime import UTC, datetime, timedelta

from tests.factories import CemepFactory


def test_deve_atualizar_timestamp_quando_comentario_for_alterado():
    cemep = CemepFactory.criar(comentario="Comentário antigo")

    atualizado_original = cemep.atualizado_em

    cemep.alterar_comentario("Novo comentário")

    assert cemep.comentario == "Novo comentário"
    assert cemep.atualizado_em > atualizado_original

from tests.factories import CemepFactory


def test_nao_deve_atualizar_timestamp_quando_comentario_for_igual():
    cemep = CemepFactory.criar(comentario="Mesmo comentário")

    atualizado_original = cemep.atualizado_em

    cemep.alterar_comentario("Mesmo comentário")

    assert cemep.atualizado_em == atualizado_original

