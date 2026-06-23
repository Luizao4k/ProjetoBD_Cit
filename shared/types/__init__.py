"""
Cada entidade tem seu próprio tip de ID.
IDs fortemente tipados — evitam confundir escolaID com projetoID
Isso impede passsar um ProjetoID onde se espera um EscolaID
"""
from typing import NewType
EscolaId   = NewType("EscolaId",   int)
RegionalId   = NewType("RegionalId",      int)
DiretorId  = NewType("DiretorId",  int)
CemepId    = NewType("CemepId",    int)
ProjetoId  = NewType("ProjetoId",  int)
EscolaProjetoId = NewType("EscolaProjetoId", int)
