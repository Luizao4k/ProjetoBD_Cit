"""
Exceções do caso de uso de Responsavel.
"""


class ResponsavelNaoEncontradoError(Exception):
    """
    Levantada quando um Responsável não é encontrado pelo
    identificador informado.
    """

    def __init__(self, responsavel_id: int) -> None:
        super().__init__(
            f"Responsavel com id={responsavel_id} não foi encontrado."
        )
        self.responsavel_id = responsavel_id
