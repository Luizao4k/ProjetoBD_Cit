"""
Cada entidade tem seu próprio tip de ID.
IDs fortemente tipados — evitam confundir escolaID com projetoID
Isso impede passsar um ProjetoID onde se espera um EscolaID
"""
from typing import NewType
EscolaId   = NewType("EscolaId",   int)
DreId      = NewType("DreId",      int)
DiretorId  = NewType("DiretorId",  int)
CemepId    = NewType("CemepId", int)
ResponsavelId = NewType("ResponsavelId", int)
TurmaCemepId = NewType("TurmaCemepId", int)
StarlinkId = NewType("StarlinkId", int)
ChromebooksId = NewType("ChromebooksId", int)
