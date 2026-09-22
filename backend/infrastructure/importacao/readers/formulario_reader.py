from __future__ import annotations

from infrastructure.importacao.protocolos import LinhaBruta


class FormularioReader:
    """
    Reader para uma única entrada fornecida por formulário.
    """

    def __init__(self, dados: LinhaBruta) -> None:
        self._dados = dados

    def ler(self):
        yield self._dados

    def total_estimado(self) -> int:
        return 1

    def validar(self) -> list[str]:
        return []