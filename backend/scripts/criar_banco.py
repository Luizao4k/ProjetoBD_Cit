"""
Cria o banco de dados SQLite da aplicação.

Responsabilidades
-----------------
- Criar o diretório de dados, se necessário.
- Criar (ou abrir) o banco SQLite.
- Inicializar todo o schema da aplicação.

Uso
---
Criar o banco padrão:

    python -m scripts.criar_banco

Criar em outro local:

    python -m scripts.criar_banco data/meu_banco.db
"""

from __future__ import annotations

import sys
from pathlib import Path

from infrastructure.database import criar_conexao, criar_schema

DEFAULT_DATABASE = Path("data/escolas.db")


def criar_banco(caminho_banco: str | Path = DEFAULT_DATABASE) -> Path:
    """
    Cria o banco SQLite e inicializa o schema.

    Parameters
    ----------
    caminho_banco:
        Caminho do arquivo do banco.

    Returns
    -------
    Path
        Caminho absoluto do banco criado.
    """
    caminho = Path(caminho_banco).resolve()

    caminho.parent.mkdir(parents=True, exist_ok=True)

    banco_existia = caminho.exists()

    conexao = criar_conexao(str(caminho))

    try:
        criar_schema(conexao)
    finally:
        conexao.close()

    if banco_existia:
        print(f"Banco já existente: {caminho}")
    else:
        print(f"Banco criado com sucesso: {caminho}")

    return caminho


def main() -> int:
    """
    Ponto de entrada do script.
    """
    caminho = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else DEFAULT_DATABASE
    )

    try:
        criar_banco(caminho)
    except Exception as erro:
        print(f"Erro ao criar banco de dados: {erro}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
