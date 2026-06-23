from infra.database.connection import get_connection
from infra.database.regional_repo import RegionalRepositorySQLite
from infra.database.escola_repo import EscolaRepositorySQLite
from infra.database.web_escola_repo import WebEscolaRepositorySQLite


class Container:
    """
    Monta e entrega as dependências do sistema.
    Os controllers pedem use cases prontos — nunca instanciam
    repositórios diretamente.
    """

    # ─────────────────────────────────────────
    # Repositórios
    # ─────────────────────────────────────────

    def regional_repo(self) -> RegionalRepositorySQLite:
        return RegionalRepositorySQLite(get_connection())

    def escola_repo(self) -> EscolaRepositorySQLite:
        return EscolaRepositorySQLite(get_connection())

    def web_escola_repo(self) -> WebEscolaRepositorySQLite:
        return WebEscolaRepositorySQLite(get_connection())

    # ─────────────────────────────────────────
    # Use cases — Regional
    # ─────────────────────────────────────────

    def criar_regional(self) -> CriarRegional:
        return CriarRegional(self.regional_repo())

    def listar_regionais(self) -> ListarRegionais:
        return ListarRegionais(self.regional_repo())

    def atualizar_regional(self) -> AtualizarRegional:
        return AtualizarRegional(self.regional_repo())

    def deletar_regional(self) -> DeletarRegional:
        return DeletarRegional(self.regional_repo())

    # ─────────────────────────────────────────
    # Use cases — Escola
    # ─────────────────────────────────────────

    def criar_escola(self) -> CriarEscola:
        return CriarEscola(self.escola_repo(), self.regional_repo())

    def buscar_escolas(self) -> BuscarEscolas:
        return BuscarEscolas(self.escola_repo())

    def atualizar_escola(self) -> AtualizarEscola:
        return AtualizarEscola(self.escola_repo(), self.regional_repo())

    def deletar_escola(self) -> DeletarEscola:
        return DeletarEscola(self.escola_repo())

    # ─────────────────────────────────────────
    # Use cases — WebEscola
    # ─────────────────────────────────────────

    def adicionar_ip(self) -> AdicionarIP:
        return AdicionarIP(self.web_escola_repo(), self.escola_repo())

    def listar_ips(self) -> ListarIPs:
        return ListarIPs(self.web_escola_repo(), self.escola_repo())

    def atualizar_ip(self) -> AtualizarIP:
        return AtualizarIP(self.web_escola_repo())

    def remover_ip(self) -> RemoverIP:
        return RemoverIP(self.web_escola_repo())


container = Container()