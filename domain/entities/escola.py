"""
Modulo contendo a entidade Escola, validações e o comportamento.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
import re

@dataclass
class Escola:
    """
    Representa uma escola cadastrada no sistema
    """

    # Identidade / dados principais
    inep: str
    nome_escola: str
    regional_id: int
    diretor_responsavel: str
    email_diretor: str
    # Dados opcionais
    designacao_starlink: Optional[str] = None
    web_escola: bool = False
    telefone: Optional[str] = None
    # Persistência
    id_escola: Optional[int] = None
    # Auditoria
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validar()

    def _validar(self):
        self._validar_inep()
        self._validar_nome()
        self._validar_regional_id()
        self._validar_email()

    def _validar_inep(self):
        if not self.inep or not self.inep.strip():
            raise ValueError("INEP não pode ser vazio.")
        if not re.fullmatch(r"\d{8}", self.inep.strip()):
            raise ValueError(
                f"INEP inválido: '{self.inep}'. "
                "Deve conter exatamente 8 dígitos numéricos."
            )

    def _validar_nome(self):
        if not self.nome_escola or not self.nome_escola.strip():
            raise ValueError("Nome da escola não pode ser vazio.")

    def _validar_regional_id(self):
        if not isinstance(self.regional_id, int): # type: ignore
            raise TypeError("regional_id deve ser um inteiro")
        if self.regional_id <= 0:
            raise ValueError("regional_id deve ser positivo")

    def _validar_email(self):
        if self.email_diretor:
            padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
            if not re.match(padrao, self.email_diretor.strip()):
                raise ValueError(
                    f"E-mail inválido: '{self.email_diretor}'.")

    # ─────────────────────────────────────────
    # Comportamentos da entidade
    # ─────────────────────────────────────────

    def atualizar(self, **campos: Any):
        """
        Atualiza campos e revalida.
        Uso: escola.atualizar(telefone="(81) 99999-0000", webEscola=True)
        """
        campos_validos = {
            "nome_escola", "regional_id", "designacao_starlink",
            "web_escola", "telefone", "diretor_responsavel", "email_diretor"
        }
        for campo, valor in campos.items():
            if campo not in campos_validos:
                raise ValueError(f"Campo não permitido para atualização: '{campo}'.")
            setattr(self, campo, valor)

        self.atualizado_em = datetime.now()
        self._validar()

    def tem_contato(self) -> bool:
        """Retorna True se a escola tem ao menos telefone ou e-mail."""
        return bool(self.telefone or self.email_diretor)

    def __str__(self):
        web = "✔" if self.web_escola else "✘"
        return f"[{self.inep}] {self.nome_escola} | Web: {web}"
