"""
Documentação OpenAPI: serve o spec (interface/openapi.yaml) cru e uma
página interativa pra explorá-lo.

Servir o .yaml diretamente (em vez de convertê-lo pra JSON no
servidor) evita precisar de uma dependência Python de parsing YAML
(pyyaml) só pra isso — o Swagger UI já sabe parsear YAML no navegador
(embute js-yaml). O arquivo em si (interface/openapi.yaml) é a única
fonte de verdade; esta rota só devolve seu conteúdo.
"""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Response

documentacao_bp = Blueprint("documentacao", __name__)

_CAMINHO_SPEC = Path(__file__).parent / "openapi.yaml"

_HTML_SWAGGER_UI = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>API de Gestão Escolar — Documentação</title>
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui.min.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.min.js"></script>
  <script>
    window.onload = () => {
      SwaggerUIBundle({
        url: "/openapi.yaml",
        dom_id: "#swagger-ui",
      });
    };
  </script>
</body>
</html>
"""


@documentacao_bp.route("/openapi.yaml")
def openapi_spec() -> Response:
    conteudo = _CAMINHO_SPEC.read_text(encoding="utf-8")
    return Response(conteudo, mimetype="text/yaml")


@documentacao_bp.route("/docs")
def documentacao_interativa() -> Response:
    return Response(_HTML_SWAGGER_UI, mimetype="text/html")
