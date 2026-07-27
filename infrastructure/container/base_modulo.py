"""
Classe base dos módulos do Container.
"""

from __future__ import annotations

import sqlite3


class BaseModulo:
    """
    Fornece a tipagem da conexão compartilhada pelos módulos do
    Container.

    A conexão é inicializada pela classe `Container`.
    """

    _conexao: sqlite3.Connection
