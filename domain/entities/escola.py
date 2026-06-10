from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re


@dataclass
class Escola:
    inep: str
    nomeEscola: str
    regional_id: int
    desigStarlink: Optional[str] = None
    webEscola: Optional[str] = None
    telefone: Optional[str] = None
    diretorResponsavel: str
    emailDiretor: str
    id: Optional[int] = None
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
        if not self.nomeEscola or not self.nomeEscola.strip():
            raise ValueError("Nome da escola não pode ser vazio.")
    
    def _validar_regional_id(self):
        if not isinstance(self.regional_id, int) or self.regional_id <= 0:
            raise ValueError("regional_id deve ser um inteiro positivo.")

    def _validar_email(self):
        if self.emailDiretor:
            padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
            if not re.match(padrao, self.emailDiretor.strip()):
                raise ValueError(
                    f"E-mail inválido: '{self.emailDiretor}'.")




    
    # ─────────────────────────────────────────
    # Comportamentos da entidade
    # ─────────────────────────────────────────

    def atualizar(self, **campos):
        """
        Atualiza campos e revalida.
        Uso: escola.atualizar(telefone="(81) 99999-0000", webEscola=True)
        """
        campos_validos = {
            "nomeEscola", "regional_id", "desigStarlink",
            "webEscola", "telefone", "diretorResponsavel", "emailDiretor"
        }
        for campo, valor in campos.items():
            if campo not in campos_validos:
                raise ValueError(f"Campo não permitido para atualização: '{campo}'.")
            setattr(self, campo, valor)

        self.atualizado_em = datetime.now()
        self._validar()

    def tem_contato(self) -> bool:
        """Retorna True se a escola tem ao menos telefone ou e-mail."""
        return bool(self.telefone or self.emailDiretor)

    def __str__(self):
        web = "✔" if self.webEscola else "✘"
        return f"[{self.inep}] {self.nomeEscola} | Web: {web}"