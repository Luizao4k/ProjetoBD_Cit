"""
Ponto de entrada da API REST.

Uso (a partir da raiz do projeto):
    python main.py [caminho/do/banco.db]

Para produção, use um servidor WSGI (gunicorn, waitress) apontando
para `apresentation.app:criar_app` em vez deste `app.run()` — o servidor
de desenvolvimento do Flask não é adequado para produção.
"""

from __future__ import annotations


from apresentation.app import criar_app


if __name__ == "__main__":
    app = criar_app("data/escolas.db")
    app.run(debug=False)
