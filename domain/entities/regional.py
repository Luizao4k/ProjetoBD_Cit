from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import unicodedata
import domain.constantes as constantes




def _normalizar(texto: str) -> str:
    """Remove acentos e converte para maiúsculas para comparação flexível."""
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode().upper().strip()


# Mapa pré-computado: nome normalizado → nome oficial
# Evita recomputar a cada validação
_MUNICIPIOS_NORMALIZADOS: dict[str, str] = {
    _normalizar(m): m for m in constantes.MUNICIPIOS_VALIDOS
}


@dataclass
class Regional:
    nome: str
    municipio: str
    tipo: str
    id: Optional[int] = None
    criado_em: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validar()

    # ─────────────────────────────────────────
    # Validações — regras que sempre valem,
    # independente de banco ou interface
    # ─────────────────────────────────────────

    def _validar(self):
        self._validar_nome()
        self._validar_municipio()
        self._validar_tipo()

    def _validar_nome(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome da regional não pode ser vazio.")

    def _validar_municipio(self):
        if not self.municipio or not self.municipio.strip():
            raise ValueError("Município não pode ser vazio.")

        entrada = _normalizar(self.municipio)

        if entrada not in _MUNICIPIOS_NORMALIZADOS:
            raise ValueError(
                f"Município '{self.municipio}' não encontrado na lista dos "
                f"{len(constantes.MUNICIPIOS_VALIDOS)} municípios válidos. "
                "Verifique a grafia ou consulte MUNICIPIOS_VALIDOS."
            )

        # Padroniza automaticamente para o nome oficial da lista
        self.municipio = _MUNICIPIOS_NORMALIZADOS[entrada]

    def _validar_tipo(self):
        if self.tipo not in constantes.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo inválido: '{self.tipo}'. "
                f"Use: {', '.join(constantes.TIPOS_VALIDOS)}."
            )

    # ─────────────────────────────────────────
    # Comportamentos da entidade
    # ─────────────────────────────────────────

    def atualizar(self, nome: str = None, municipio: str = None, tipo: str = None) -> None:
        """Atualiza campos e revalida as regras de negócio."""
        if nome is not None:
            self.nome = nome
        if municipio is not None:
            self.municipio = municipio
        if tipo is not None:
            self.tipo = tipo
        self._validar()

    def eh_dre(self) -> bool:
        return self.tipo == "DRE"

    def eh_nte(self) -> bool:
        return self.tipo == "NTE"

    def __str__(self):
        return f"[{self.tipo}] {self.nome} — {self.municipio}"