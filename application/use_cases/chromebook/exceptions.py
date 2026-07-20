"""
Exceções do caso de uso de Chromebook.
"""


class ChromebookNaoEncontradoError(Exception):
    """
    Levantada quando um registro de Chromebook não é encontrado
    pelo identificador informado.
    """

    def __init__(self, chromebook_id: int) -> None:
        super().__init__(
            f"Chromebook com id={chromebook_id} não foi encontrado."
        )
        self.chromebook_id = chromebook_id
