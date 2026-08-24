"""
Ponto de entrada da API REST.

Uso (a partir da raiz do projeto):
    python main.py [caminho/do/banco.db]

Para produção, use um servidor WSGI (gunicorn, waitress) apontando
para `interface.app:criar_app` em vez deste `app.run()` — o servidor
de desenvolvimento do Flask não é adequado para produção.
"""

from __future__ import annotations

import sys

from interface.app import criar_app

if __name__ == "__main__":
    caminho_banco = sys.argv[1] if len(sys.argv) > 1 else "escolas.db"
    app = criar_app(caminho_banco)
    app.run(debug=False)
