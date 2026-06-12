from domain.entities.escola import Escola
from domain.repositories.escola_repository import EscolaRepository
from domain.repositories.regional_repository import RegionalRepository

class CriarEscola:
    def __init__(self, repo: EscolaRepository, repo_regional: RegionalRepository):
        self._repo = repo
        self._repo_regional = repo_regional
    

    def executar(self, inep: str, nomeEscola: str, regional_id, **opcionais) -> Escola:
        if self._repo.inep_existe(inep):
            raise ValueError(f"INEP '{inep}' já esta cadastrado.")

        if not self._repo_regional.buscar_por_id(regional_id):
            raise ValueError(f"Regional {regional_id} não encontrada.")
        
        escola = Escola(inep=inep, nomeEscola=nomeEscola, regional_id=regional_id, **opcionais)
        return self._repo.salvar(escola)