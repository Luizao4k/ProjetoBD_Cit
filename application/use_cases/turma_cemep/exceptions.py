"""
Exceções do caso de uso de TurmaCemep.
"""


class TurmaCemepNaoEncontradaError(Exception):
    """
    Levantada quando uma Turma não é encontrada pelo
    identificador informado.
    """

    def __init__(self, turma_id: int) -> None:
        super().__init__(f"TurmaCemep com id={turma_id} não foi encontrada.")
        self.turma_id = turma_id
