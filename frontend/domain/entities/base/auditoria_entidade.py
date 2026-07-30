"""
Classe base para entidades com auditoria.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(kw_only=True)
class AuditoriaEntidade:
    """
    Fornece campos e comportamento de auditoria para entidades do domínio.

    IMPORTANTE: esta classe usa kw_only=True porque seus campos
    (criado_em, atualizado_em) têm valor padrão. Qualquer entidade
    filha que declare campos SEM valor padrão (ex: id, nome) deve
    OBRIGATORIAMENTE também usar @dataclass(kw_only=True), senão o
    Python lança erro na importação:

        TypeError: non-default argument 'x' follows default argument

    Isso ocorre porque dataclasses geram o __init__ com os campos do
    pai primeiro e do filho depois, e Python não permite argumento
    obrigatório após argumento com default numa assinatura posicional.
    kw_only=True remove essa restrição ao tornar todos os campos
    somente-por-nome.

    Ao criar uma nova entidade herdando desta classe, use:

        @dataclass(kw_only=True)
        class MinhaEntidade(AuditoriaEntidade):
            ...
    """

    criado_em: datetime = field(default_factory=lambda: datetime.now(UTC))
    atualizado_em: datetime = field(default_factory=lambda: datetime.now(UTC))

    def _marcar_tempo(self) -> None:
        """
        Atualiza o timestamp da última modificação da entidade.
        """
        self.atualizado_em = datetime.now(UTC)
