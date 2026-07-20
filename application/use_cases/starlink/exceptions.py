"""
Exceções do caso de uso de Starlink.
"""


class StarlinkNaoEncontradoError(Exception):
    """
    Levantada quando uma designação de Starlink não é encontrada
    pelo identificador informado.
    """

    def __init__(self, starlink_id: int) -> None:
        super().__init__(f"Starlink com id={starlink_id} não foi encontrado.")
        self.starlink_id = starlink_id
