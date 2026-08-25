# API — Sistema de Gestão Escolar (CIT/Pará)

Guia de consumo da API REST. Complementa o [`apresentation/openapi.yaml`](apresentation/openapi.yaml) — spec formal, navegável em `/docs` (Swagger UI) com o servidor rodando — com convenções, exemplos reais de request/response e comportamentos que a spec não descreve em prosa. Todos os exemplos abaixo foram capturados de execução real da API, não escritos à mão.

## Visão geral

- **Stack**: Python, Flask, SQLite, arquitetura em camadas (`domain` → `application` → `infrastructure` → `apresentation`)
- **Formato**: JSON em toda requisição e resposta (`Content-Type: application/json`)
- **Rodando localmente**: `python main.py [caminho/do/banco.db]` → `http://localhost:5000`
- **Spec interativa**: `GET /docs` (Swagger UI) · `GET /openapi.yaml` (spec bruta)

8 recursos, todos com CRUD completo (`POST`, `GET` lista, `GET /{id}`, `PUT /{id}` parcial, `DELETE /{id}`): **DRE**, **Escola**, **Diretor**, **CEMEP**, **Chromebook**, **Starlink**, **Responsável**, **Turma CEMEP**.

## Modelo de relacionamento

```
DRE (1) ──< (N) Escola
Escola (1) ──── (1) Diretor       1:1 — uma Escola tem no máximo um Diretor
Escola (1) ──── (1) CEMEP         1:1 — uma Escola tem no máximo um CEMEP
Escola (1) ──── (1) Chromebook    1:1 — um registro de kit por Escola
Escola (1) ──< (N) Starlink       1:N — única relação de Escola que aceita vários
CEMEP  (1) ──< (N) Responsável
Responsável (1) ──< (N) TurmaCemep
```

Isso importa na prática porque **não existe cascade delete** — exclusão é bloqueada enquanto houver dependentes (ver seção de erros). Para apagar uma DRE, primeiro é preciso apagar ou realocar suas Escolas.

## Convenções gerais

**Campos de auditoria** — todo objeto de saída tem `id`, `criado_em` e `atualizado_em`, em ISO 8601 com offset UTC e microssegundos:
```json
"criado_em": "2026-08-25T09:38:56.599512+00:00"
```

**Chaves em ordem alfabética** — efeito do serializador padrão do Flask (`sort_keys=True`), não uma garantia contratual da API. Não vale a pena depender da ordem das chaves no client.

**`PUT` é sempre parcial** — campos omitidos do corpo não são alterados. Cada recurso tem campos imutáveis específicos (ex.: `inep`, `tipo`, `municipio` e `dre_id` de Escola nunca mudam depois de criados); enviá-los num `PUT` não gera erro, eles são simplesmente ignorados.

**Sem paginação nem filtro** — todo `GET` de listagem retorna o array completo, sempre. Não existe `?page=`, `?limit=` ou `?filtro=`.

**Corpo malformado vira corpo vazio** — se o JSON enviado for inválido, a API não devolve um erro dedicado de "JSON malformado": o parse falha silenciosamente e o corpo é tratado como `{}`. Num `POST` isso quase sempre aciona o erro 400 de campo obrigatório ausente; num `PUT`, significa que nenhum campo é alterado (resposta 200 normal, sem mudanças).

**Cada requisição é sua própria transação** — uma falha no meio de uma requisição desfaz qualquer escrita pendente dela. Não é necessário nenhum tratamento compensatório no client.

## Regras de validação por campo (Value Objects)

| Campo | Regra | Normalização aplicada |
|---|---|---|
| `nome` — DRE, Escola, Diretor, Responsável — **e também** `designacao` (Starlink) e `nome_turma` (Turma CEMEP), que usam o mesmo Value Object | não pode ser vazio; máx. 255 caracteres | acentos removidos + **CAIXA ALTA** (`"João"` → `"JOAO"`) |
| `telefone` (DRE, Diretor) | 8 a 11 dígitos após remover não-dígitos | só os dígitos ficam (`"(94) 3324-1234"` → `"9433241234"`) |
| `email` (Diretor) | precisa bater no padrão `usuario@dominio.tld` | vira minúsculas, sem espaço nas pontas |
| `inep` (Escola) | exatamente 8 dígitos numéricos | nenhuma — validação estrita |
| `municipio` (Escola) | precisa ser um dos 144 municípios do Pará (comparação sem diferenciar maiúsculas/minúsculas) | normalizado pra grafia oficial da lista, **mantém acento** |
| `endereco` (Escola) | não pode ser vazio | trim |
| `comentario` (CEMEP) | não pode ser vazio; máx. 255 caracteres | trim |
| `kit_aluno` / `kit_professor` (Chromebook) | inteiro maior que zero, se enviado | — |

> ⚠️ **`nome` normaliza diferente de `municipio`**: nome perde acento e vira maiúsculo; município mantém acento e vira a grafia oficial da lista fechada. É intencional (nome é texto livre de exibição, município é chave contra uma lista fixa), mas fácil de esquecer ao construir a UI — o valor que volta na resposta não é sempre igual ao que foi enviado.

## Erros — referência completa

Toda resposta de erro segue o mesmo formato:
```json
{
  "erro": "NomeDaClasseDaExcecao",
  "mensagem": "Descrição legível do que houve."
}
```

| Status | Quando ocorre | Exemplos de `erro` |
|---|---|---|
| 400 | Campo obrigatório ausente no corpo | `RequisicaoInvalidaError` |
| 400 | Valor viola regra de um Value Object | `NomeInvalidoError`, `EmailInvalidoError`, `InepInvalidoError`, `TelefoneInvalidoError`, `QuantidadeInvalidaError`, `ComentarioInvalidoError`, `EnderecoInvalidoError`, `MunicipioInvalidoError` |
| 400 | `tipo` de Escola fora de `ESTADUAL`/`MUNICIPAL` | `ValueError` — mensagem crua do Enum do Python, não uma exceção de domínio própria |
| 404 | Nenhum registro com o `id` da URL | `DreNaoEncontradaError`, `EscolaNaoEncontradaError`, `DiretorNaoEncontradoError`, `CemepNaoEncontradoError`, `ChromebookNaoEncontradoError`, `StarlinkNaoEncontradoError`, `ResponsavelNaoEncontradoError`, `TurmaCemepNaoEncontradaError` |
| 404 | Id referenciado no corpo (`dre_id`, `escola_id`, `cemep_id`, `responsavel_id`) não existe | mesma família acima |
| 404 | Rota inexistente (nativo do Flask/Werkzeug) | `Not Found` |
| 405 | Método HTTP não suportado naquela rota (nativo do Flask/Werkzeug) | `Method Not Allowed` |
| 409 | Violação de unicidade — relação 1:1 já ocupada ou INEP repetido | `InepJaCadastradoError`, `EscolaJaPossuiDiretorError`, `EscolaJaPossuiCemepError`, `EscolaJaPossuiChromebookError` |
| 409 | Exclusão bloqueada por dependentes | `DrePossuiEscolasError`, `EscolaPossuiDiretorError`, `EscolaPossuiCemepError`, `EscolaPossuiChromebookError`, `EscolaPossuiStarlinksError`, `CemepPossuiResponsaveisError`, `ResponsavelPossuiTurmasError` |
| 500 | Falha de infraestrutura (conexão/persistência) | `PersistenciaError` e subclasses |

> `Starlink`, `Responsável` e `Turma CEMEP` **não** têm 409 de duplicidade na criação — uma Escola pode ter vários Starlinks, um CEMEP vários Responsáveis, um Responsável várias Turmas.

### Exemplos reais

**Campo obrigatório ausente**
```json
400 Bad Request
{"erro": "RequisicaoInvalidaError", "mensagem": "Campo(s) obrigatório(s) ausente(s): inep, tipo, municipio, dre_id."}
```

**Value Object inválido**
```json
400 Bad Request
{"erro": "InepInvalidoError", "mensagem": "INEP deve ter exatamente 8 dígitos numéricos. Recebido: 'abc'"}
```

**Enum inválido**
```json
400 Bad Request
{"erro": "ValueError", "mensagem": "'FEDERAL' is not a valid TipoEscola"}
```

**Referência inexistente**
```json
404 Not Found
{"erro": "DreNaoEncontradaError", "mensagem": "DRE com id=99999 não foi encontrado(a)."}
```

**Duplicidade**
```json
409 Conflict
{"erro": "InepJaCadastradoError", "mensagem": "Já existe uma Escola cadastrada com esse código INEP."}
```

**Exclusão bloqueada por dependente**
```json
409 Conflict
{"erro": "DrePossuiEscolasError", "mensagem": "Violação de chave estrangeira: existem Escolas vinculadas à DRE."}
```

## Endpoints por recurso

### DRE

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/dres` | Cria uma DRE |
| `GET` | `/dres` | Lista todas |
| `GET` | `/dres/{id}` | Busca por id |
| `PUT` | `/dres/{id}` | Atualiza (parcial) |
| `DELETE` | `/dres/{id}` | Remove — `409` se houver Escola vinculada |

Campos: `nome` obrigatório · `telefone` opcional.

```http
POST /dres
{"nome": "5ª URE - Marabá", "telefone": "(94) 3324-1234"}
```
```json
201 Created
{
  "atualizado_em": "2026-08-25T09:38:56.596472+00:00",
  "criado_em": "2026-08-25T09:38:56.596465+00:00",
  "id": 1,
  "nome": "5A URE - MARABA",
  "telefone": "9433241234"
}
```

### Escola

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/escolas` | Cria uma Escola |
| `GET` | `/escolas` | Lista todas |
| `GET` | `/escolas/{id}` | Busca por id |
| `PUT` | `/escolas/{id}` | Atualiza — só `nome` e `endereco` são alteráveis |
| `DELETE` | `/escolas/{id}` | Remove — `409` se tiver Diretor, CEMEP, Chromebook ou Starlink vinculado |

Campos obrigatórios: `inep`, `nome`, `tipo` (`ESTADUAL`\|`MUNICIPAL`), `municipio`, `dre_id` · opcional: `endereco`. `inep`, `tipo`, `municipio` e `dre_id` são **imutáveis** após a criação.

```http
POST /escolas
{
  "inep": "15000001", "nome": "EEEFM Prof. João Silva",
  "tipo": "ESTADUAL", "municipio": "Marabá", "dre_id": 1,
  "endereco": "Rua das Escolas, 100"
}
```
```json
201 Created
{
  "atualizado_em": "2026-08-25T09:38:56.599515+00:00",
  "criado_em": "2026-08-25T09:38:56.599512+00:00",
  "dre_id": 1,
  "endereco": "Rua das Escolas, 100",
  "id": 1,
  "inep": "15000001",
  "municipio": "Marabá",
  "nome": "EEEFM PROF. JOAO SILVA",
  "tipo": "ESTADUAL"
}
```

Erros próprios: `404 DreNaoEncontradaError` (dre_id inexistente) · `409 InepJaCadastradoError` (INEP repetido).

### Diretor

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/diretores` | Cria um Diretor |
| `GET` | `/diretores` | Lista todos |
| `GET` | `/diretores/{id}` | Busca por id |
| `PUT` | `/diretores/{id}` | Atualiza — `escola_id` não é alterável |
| `DELETE` | `/diretores/{id}` | Remove |

Campos obrigatórios: `escola_id`, `nome` · opcionais: `telefone`, `email`.

Erros próprios: `404 EscolaNaoEncontradaError` (escola_id inexistente) · `409 EscolaJaPossuiDiretorError` (relação Escola↔Diretor é 1:1).

### CEMEP

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/cemeps` | Cria um CEMEP |
| `GET` | `/cemeps` | Lista todos |
| `GET` | `/cemeps/{id}` | Busca por id |
| `PUT` | `/cemeps/{id}` | Atualiza (só `comentario`) |
| `DELETE` | `/cemeps/{id}` | Remove — `409` se tiver Responsável vinculado |

Campos: `escola_id` obrigatório · `comentario` opcional.

Erros próprios: `404 EscolaNaoEncontradaError` · `409 EscolaJaPossuiCemepError` (criação, relação 1:1) · `409 CemepPossuiResponsaveisError` (exclusão).

### Chromebook

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/chromebooks` | Cria um registro de Chromebook |
| `GET` | `/chromebooks` | Lista todos |
| `GET` | `/chromebooks/{id}` | Busca por id |
| `PUT` | `/chromebooks/{id}` | Atualiza |
| `DELETE` | `/chromebooks/{id}` | Remove — sem restrição de dependentes |

Campos: `escola_id` obrigatório · `kit_aluno`, `kit_professor` opcionais (inteiros positivos, se enviados).

Erros próprios: `404 EscolaNaoEncontradaError` · `409 EscolaJaPossuiChromebookError` (criação, relação 1:1).

### Starlink

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/starlinks` | Cria uma designação de Starlink |
| `GET` | `/starlinks` | Lista todos |
| `GET` | `/starlinks/{id}` | Busca por id |
| `PUT` | `/starlinks/{id}` | Atualiza |
| `DELETE` | `/starlinks/{id}` | Remove — sem restrição de dependentes |

Campos obrigatórios: `escola_id`, `designacao` (passa pelas mesmas regras de `nome` — acento removido, vira maiúsculo).

Única relação **1:N** de Escola — sem 409 de duplicidade na criação. Erro próprio: `404 EscolaNaoEncontradaError`.

### Responsável

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/responsaveis` | Cria um Responsável |
| `GET` | `/responsaveis` | Lista todos |
| `GET` | `/responsaveis/{id}` | Busca por id |
| `PUT` | `/responsaveis/{id}` | Atualiza |
| `DELETE` | `/responsaveis/{id}` | Remove — `409` se tiver Turma vinculada |

Campos obrigatórios: `cemep_id`, `nome`.

Erros próprios: `404 CemepNaoEncontradoError` (cemep_id inexistente) · `409 ResponsavelPossuiTurmasError` (exclusão).

### Turma CEMEP

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/turmas-cemep` | Cria uma Turma |
| `GET` | `/turmas-cemep` | Lista todas |
| `GET` | `/turmas-cemep/{id}` | Busca por id |
| `PUT` | `/turmas-cemep/{id}` | Atualiza |
| `DELETE` | `/turmas-cemep/{id}` | Remove — sem restrição de dependentes |

Campos obrigatórios: `responsavel_id`, `nome_turma` (passa pelas mesmas regras de `nome`).

Erro próprio: `404 ResponsavelNaoEncontradoError` (responsavel_id inexistente).

## Fora do escopo atual da API

A camada de aplicação já tem casos de uso prontos para busca por relação — achar o Diretor de uma Escola, o CEMEP de uma Escola, o Chromebook de uma Escola, as Escolas de uma DRE — mas nenhum está ligado a uma rota HTTP hoje (nenhum controller/route os chama). Se endpoints como `GET /escolas/{id}/diretor` aparecerem no futuro, é esse código que já existe pra alimentá-los.

---

*Gerado a partir da leitura do código-fonte e de execução real da API (não só do `openapi.yaml`) em 25/08/2026. Para a spec formal e sempre sincronizada com o código, use `/docs` com o servidor rodando.*
