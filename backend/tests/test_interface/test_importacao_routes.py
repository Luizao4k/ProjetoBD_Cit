"""
Testes de integração HTTP da rota de Importação — via Flask test
client, sem servidor real (mesmo padrão de test_dre_routes.py).

Cobre a ponte entre upload multipart/form-data e os scripts de
importação já testados fim-a-fim em
tests/test_importacao/test_scripts_integracao.py; não reexplica as
regras de negócio de cada Mapper/Use Case, só que o controller sabe
recebê-las via HTTP, delegar pro script certo e devolver um relatório
em JSON.
"""

from __future__ import annotations

import io

from openpyxl import Workbook


def _csv(cabecalho: list[str], linhas: list[dict[str, str]]) -> tuple[io.BytesIO, str]:
    texto = ",".join(cabecalho) + "\r\n"
    for linha in linhas:
        texto += ",".join(linha.get(coluna, "") for coluna in cabecalho) + "\r\n"
    return io.BytesIO(texto.encode("utf-8")), "arquivo.csv"


def _xlsx(cabecalho: list[str], linhas: list[dict[str, str]]) -> tuple[io.BytesIO, str]:
    workbook = Workbook()
    planilha = workbook.active
    planilha.append(cabecalho)
    for linha in linhas:
        planilha.append([linha.get(coluna, "") for coluna in cabecalho])
    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer, "arquivo.xlsx"


def _importar(client, tipo, arquivo_e_nome):
    arquivo, nome = arquivo_e_nome
    return client.post(
        "/importacao",
        data={"tipo": tipo, "arquivo": (arquivo, nome)},
        content_type="multipart/form-data",
    )


# ---------------------------------------------------------------------
# Validação da requisição
# ---------------------------------------------------------------------


def test_tipo_invalido_retorna_400(client):
    resposta = _importar(client, "tipo-que-nao-existe", _csv(["nome"], []))

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "RequisicaoInvalidaError"


def test_arquivo_ausente_retorna_400(client):
    resposta = client.post(
        "/importacao", data={"tipo": "dre"}, content_type="multipart/form-data"
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "RequisicaoInvalidaError"


def test_extensao_nao_suportada_retorna_400(client):
    resposta = client.post(
        "/importacao",
        data={"tipo": "dre", "arquivo": (io.BytesIO(b"nome\ndre belem\n"), "dres.txt")},
        content_type="multipart/form-data",
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "RequisicaoInvalidaError"


def test_coluna_obrigatoria_faltando_retorna_400_arquivo_invalido(client):
    resposta = _importar(client, "dre", _csv(["telefone"], [{"telefone": "91999998888"}]))

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "ArquivoInvalidoError"


# ---------------------------------------------------------------------
# Importação bem-sucedida (CSV e Excel)
# ---------------------------------------------------------------------


def test_importar_dres_csv_retorna_relatorio_com_sucesso_e_falha(client):
    resposta = _importar(
        client,
        "dre",
        _csv(
            ["nome", "telefone"],
            [
                {"nome": "dre belem", "telefone": "91999998888"},
                {"nome": "   ", "telefone": ""},  # nome vazio -> falha
            ],
        ),
    )

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["tipo"] == "dre"
    assert corpo["sucessos"] == 1
    assert corpo["erros"] == 1
    assert corpo["total_processado"] == 2
    assert corpo["taxa_sucesso"] == 0.5
    assert len(corpo["falhas"]) == 1
    assert corpo["falhas"][0]["tipo_erro"] == "NomeInvalidoError"
    assert corpo["falhas"][0]["numero_linha"] == 2
    assert corpo["falhas"][0]["dados_originais"]["nome"] == "   "

    # persistiu no MESMO banco usado pelo resto da API (não um
    # arquivo à parte) — prova de que app.config["CAMINHO_BANCO"]
    # chegou corretamente ao controller.
    listagem = client.get("/dres").get_json()
    assert [dre["nome"] for dre in listagem] == ["DRE BELEM"]


def test_importar_dres_via_excel_funciona_igual_ao_csv(client):
    resposta = _importar(
        client, "dre", _xlsx(["nome", "telefone"], [{"nome": "dre maraba", "telefone": ""}])
    )

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["sucessos"] == 1
    assert corpo["erros"] == 0


def test_importar_sem_falhas_retorna_lista_de_falhas_vazia(client):
    resposta = _importar(client, "dre", _csv(["nome"], [{"nome": "dre belem"}]))

    assert resposta.status_code == 200
    assert resposta.get_json()["falhas"] == []


# ---------------------------------------------------------------------
# Cadeia de dependência entre entidades, via rota HTTP
# ---------------------------------------------------------------------


def test_cadeia_dre_escola_via_rota_de_importacao(client):
    resposta_dre = _importar(client, "dre", _csv(["nome"], [{"nome": "dre belem"}]))
    assert resposta_dre.get_json()["sucessos"] == 1

    resposta_escola = _importar(
        client,
        "escolas",
        _csv(
            ["inep", "nome", "tipo", "municipio", "dre_nome"],
            [
                {
                    "inep": "12345678",
                    "nome": "Escola A",
                    "tipo": "MUNICIPAL",
                    "municipio": "Belem",
                    "dre_nome": "dre belem",
                }
            ],
        ),
    )

    assert resposta_escola.status_code == 200
    assert resposta_escola.get_json()["sucessos"] == 1
    assert [e["inep"] for e in client.get("/escolas").get_json()] == ["12345678"]
