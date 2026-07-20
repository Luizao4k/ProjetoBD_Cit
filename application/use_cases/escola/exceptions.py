"""
Exceções do caso de uso de Escola.
"""


class EscolaNaoEncontradaError(Exception):
    """
    Levantada quando uma Escola não é encontrada pelo
    identificador informado.
    """

    def __init__(self, escola_id: int) -> None:
        super().__init__(f"Escola com id={escola_id} não foi encontrada.")
        self.escola_id = escola_id
