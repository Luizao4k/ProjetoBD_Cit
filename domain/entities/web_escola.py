from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class WebEscola:
    escola_id: int              #OBRIGATORIO
    ip: str                     #OBRIGATORIO
    id: Optional[int] = None    #OPCIONAL
    criado_em: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validar()
    
    def _validar(self):
        self._validar_escola_id()
        self._validar_ip()


    def _validar_escola_id(self):
        if not isinstance(self.escola_id, int) or self.escola_id <= 0:
            raise ValueError("escola_id deve ser um inteiro positivo.")
    

    def _validar_ip(self):
        if not self.ip or not self.ip.strip():
            raise ValueError("Ip não pode ser vazio")




    def atualizar_ip(self, novo_ip: str) -> None:
        """ATUALIZA O IP E REVALIDA"""
        self.ip = novo_ip 
        self._validar_ip()

    def __str__(self):
        return f"[WebEscola] escola_id={self.escola_id} | IP:{self.ip}"