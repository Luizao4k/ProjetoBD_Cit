# Arquitetura — Sistema de Gestão Escolar (CIT/Pará)

Documento de referência sobre como o backend é organizado: as camadas, o sentido das dependências entre elas, os padrões usados em cada uma e os porquês por trás das decisões mais importantes. Complementa o [`API.md`](API.md) (consumo da API HTTP) e o [`README.md`](README.md) (visão de produto) — aqui o foco é em como o código por dentro é montado.

Tudo abaixo foi extraído do código-fonte real, não do diagrama do README (que ficou desatualizado — ver seção final).

## Visão geral

O projeto segue **Clean Architecture** com influência de **Domain-Driven Design**: quatro camadas concêntricas, mais um módulo `shared` atravessando todas. A regra que organiza tudo é a **Regra de Dependência**: código de uma camada só pode importar de camadas mais internas, nunca o contrário.

```
        ┌─────────────────────────────────────────┐
        │           apresentation                   │  Flask: controllers, routes, HTTP
        │  ┌─────────────────────────────────────┐  │
        │  │          infrastructure               │  │  SQLite, Container (DI), import/export
        │  │  ┌─────────────────────────────────┐ │  │
        │  │  │           application            │ │  │  Use Cases, DTOs
        │  │  │  ┌─────────────────────────────┐│ │  │
        │  │  │  │           domain             ││ │  │  Entidades, Value Objects, regras
        │  │  │  └─────────────────────────────┘│ │  │
        │  │  └─────────────────────────────────┘ │  │
        │  └─────────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                  shared (types, exceptions) — usado por todas as camadas
```

`domain` não importa nada das outras três. `application` só importa de `domain`. `infrastructure` implementa interfaces que `domain` declara (inversão de dependência — é por isso que `application` pode usar um repositório sem nunca importar `sqlite3`). `apresentation` é a única camada que conhece Flask.

## Estrutura de pastas real

```
backend/
├── domain/
│   ├── entities/          # Entidades: Dre, Escola, Diretor, Cemep, Chromebook,
│   │   └── base/          #   Responsavel, TurmaCemep, Starlink + AuditoriaEntidade (base)
│   ├── value_objects/      # Nome, Telefone, Email, Inep, Municipio, Endereco,
│   │                       #   Quantidade, Comentario — cada um com sua validação
│   ├── repositories/       # Interfaces (ABC) — um contrato por entidade
│   ├── enums/               # TipoEscola, StatusEscolaProjeto (não usado ainda)
│   ├── limite.py           # MAX_LEN = 255
│   ├── municipios_validos.py  # lista fechada dos 144 municípios do Pará
│   └── entidade_constantes.py
│
├── application/
│   └── use_cases/
│       ├── dre/ escola/ diretor/ cemep/ chromebook/ responsavel/
│       │   starlink/ turma_cemep/     # uma pasta por entidade
│       │   ├── dtos.py                #   Input/Output DTOs (dataclasses frozen)
│       │   ├── criar_*.py             #   1 classe = 1 caso de uso
│       │   ├── atualizar_*.py
│       │   ├── remover_*.py
│       │   ├── listar_*.py
│       │   ├── buscar_*_por_id.py
│       │   └── buscar_*_por_<relacao>.py  # existem, mas nem todos têm rota HTTP (ver seção final)
│
├── infrastructure/
│   ├── database/sqlite/
│   │   ├── connection.py       # único lugar que sabe que o banco é SQLite
│   │   ├── schema.py            # DDL das 8 tabelas
│   │   ├── _util.py             # tradução IntegrityError -> exceção de domínio
│   │   ├── transacao.py         # context manager — sem chamador ativo hoje (ver histórico)
│   │   ├── gerenciador_transacao.py  # commit/rollback por linha, usado pela importação
│   │   └── repositories/        # implementação concreta de cada *Repository
│   ├── container/
│   │   ├── container.py         # Composition Root
│   │   ├── base_modulo.py
│   │   └── *_modulo.py          # um mixin por entidade
│   ├── importacao/               # pipeline de ETL (CSV/Excel -> banco)
│   └── exporters/                # excel_exporter.py — stub vazio, Fase futura
│
├── apresentation/
│   ├── app.py                    # app factory: criar_app()
│   ├── controllers/               # um módulo de funções por entidade
│   ├── routes/                    # um Blueprint por entidade
│   ├── erros.py                   # tratamento global de exceção -> HTTP
│   ├── serializacao.py            # DTO -> dict JSON-seguro
│   ├── documentacao.py            # serve /docs (Swagger UI) e /openapi.yaml
│   └── openapi.yaml               # spec OpenAPI 3.0.3 escrita à mão
│
├── shared/
│   ├── exceptions/                 # DomainError, ApplicationError, InfrastructureError + subclasses
│   └── types/                      # EscolaId, DreId... (NewType sobre int)
│
├── scripts/                        # CLI de importação em lote (usa a mesma application, sem Flask)
├── tests/                          # espelha as camadas acima (ver seção própria)
├── data/DRE.csv
└── main.py                         # ponto de entrada: python main.py [banco.db]
```

## Camada: Domain

Não depende de nada — nem de `application`, nem de banco, nem do Flask. É puro Python.

**Entidades** (`domain/entities/`) são `@dataclass(kw_only=True)` que herdam de `AuditoriaEntidade`, a base que fornece `criado_em`/`atualizado_em` e o método `_marcar_tempo()`:

```python
@dataclass(kw_only=True)
class AuditoriaEntidade:
    criado_em: datetime = field(default_factory=lambda: datetime.now(UTC))
    atualizado_em: datetime = field(default_factory=lambda: datetime.now(UTC))

    def _marcar_tempo(self) -> None:
        self.atualizado_em = datetime.now(UTC)
```

Isso exige que **toda** entidade filha também use `kw_only=True` — se não usar, o Python levanta `TypeError: non-default argument follows default argument` na importação, porque dataclasses geram `__init__` com campos do pai primeiro (que têm default) e do filho depois (que não têm). O próprio arquivo documenta essa armadilha no docstring, para quem for criar uma nova entidade.

Campos imutáveis (ex.: `inep`, `tipo`, `municipio` de `Escola`) não têm método `alterar_*` — a imutabilidade é garantida pela **ausência** de uma forma de mudá-los, não por uma checagem em runtime.

**Value Objects** (`domain/value_objects/`) validam no `__post_init__` e levantam uma exceção de domínio própria se o valor for inválido (`NomeInvalidoError`, `InepInvalidoError`, etc.). Cada um encapsula sua própria normalização — `Nome` remove acento e vira maiúsculo, `Municipio` normaliza para a grafia oficial da lista fechada, `Telefone` mantém só dígitos. Regras completas de cada um estão no `API.md`.

**Repositórios** (`domain/repositories/`) são interfaces (`ABC` + `@abstractmethod`), não implementações — é aqui que a Regra de Dependência é invertida: `domain` declara o contrato, `infrastructure` o implementa.

```python
class EscolaRepository(ABC):
    @abstractmethod
    def salvar(self, escola: Escola) -> Escola: ...
    @abstractmethod
    def buscar_por_id(self, escola_id: EscolaId) -> Escola | None: ...
    # ...
```

Um caso de uso depende de `EscolaRepository` (a interface), nunca de `SqliteEscolaRepository` (a implementação) — é isso que torna trivial trocar de SQLite para outro banco no futuro (Fase 7 do ROADMAP) sem tocar em `application` ou `domain`.

## Camada: Application

Um caso de uso = uma classe = uma ação = um método `executar()`. Nenhuma classe faz mais de uma coisa (criar + validar + notificar, por exemplo) — cada operação (`Criar*`, `Atualizar*`, `Remover*`, `Listar*`, `Buscar*PorId`) é sua própria classe, injetada com a interface do repositório via construtor:

```python
class CriarEscolaUseCase:
    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarEscolaInput) -> EscolaOutput:
        escola = Escola(
            id=None,
            inep=Inep(dados.inep),      # validação do Value Object acontece aqui
            nome=Nome(dados.nome),
            tipo=TipoEscola(dados.tipo), # ValueError puro se fora do enum
            municipio=Municipio(dados.municipio),
            dre_id=DreId(dados.dre_id),
            endereco=Endereco(dados.endereco) if dados.endereco else None,
        )
        escola_criada = self._repositorio.salvar(escola)
        ...
        return EscolaOutput(...)
```

Repare que o Use Case não valida nada diretamente — ele delega a validação aos Value Objects ao construir a entidade. Isso mantém a regra de negócio num único lugar (`domain`), não espalhada entre Use Case e Value Object.

**DTOs** (`dtos.py` de cada pasta) são `@dataclass(frozen=True, slots=True)` — imutáveis, sem métodos, só dados. `CriarXInput`, `AtualizarXInput` (campos opcionais para suportar atualização parcial) e `XOutput`. Nunca expõem os Value Objects diretamente — sempre tipos primitivos (`str`, `int`), o que mantém `domain` invisível para quem consome um DTO fora dessa camada.

**Casos de uso "buscar por relação"** (`buscar_diretor_por_escola`, `buscar_cemep_por_escola`, `buscar_chromebook_por_escola`, `buscar_escolas_por_dre`) existem, têm testes próprios, mas **nenhum está conectado a uma rota HTTP hoje** — ver seção final.

## Camada: Infrastructure

Quatro sub-áreas com responsabilidades distintas.

### `database/sqlite/`

`connection.py` é o único arquivo do projeto que sabe que o banco é SQLite (`sqlite3.connect(..., check_same_thread=False)`, `PRAGMA foreign_keys = ON`, `row_factory = sqlite3.Row`). `schema.py` guarda o DDL das 8 tabelas — datas viram `TEXT` em ISO 8601, relações 1:1 (Diretor/CEMEP/Chromebook com Escola) são impostas por `UNIQUE` na foreign key.

Cada `Sqlite*Repository` implementa a interface correspondente de `domain/repositories/` e faz a **tradução de exceção**: um `sqlite3.IntegrityError` genérico vira uma exceção de domínio específica, usando o código de erro do SQLite (não o texto da mensagem, que muda por idioma/locale — isso já foi bug uma vez, ver seção de decisões):

```python
except sqlite3.IntegrityError as exc:
    if eh_violacao_unique(exc):
        raise InepJaCadastradoError() from exc
    if eh_violacao_foreign_key(exc):
        raise DreNaoEncontradaError(escola.dre_id) from exc
```

Para `remover()`, o SQLite não diz *qual* tabela bloqueou a exclusão (a mensagem de FK violation é genérica) — `SqliteEscolaRepository._identificar_bloqueio()` faz uma consulta explícita em cada uma das 4 tabelas dependentes (diretores, cemeps, chromebooks, starlinks) até achar a culpada, e só então levanta o erro certo (`EscolaPossuiDiretorError`, etc.).

Nenhum repositório comita a própria escrita — isso é decisão de quem chama (`Container.finalizar()` numa requisição HTTP, `GerenciadorDeTransacaoSqlite` numa importação linha a linha). Um `INSERT`/`UPDATE`/`DELETE` fica pendente até o chamador decidir confirmar.

### `container/`

Composition Root do projeto — description completa na próxima seção.

### `importacao/`

Pipeline de ETL para carregar CSV/Excel no banco, reaproveitando os mesmos Use Cases de `application` (não duplica regra de negócio). Arquitetura própria, resumida aqui — ver os arquivos-fonte para o detalhe completo, que já vem bem comentado:

- `protocolos.py` define 4 `Protocol` (interface estrutural — duck typing checado estaticamente, sem exigir herança): `Reader` (lê linhas cruas), `Mapper` (linha crua → DTO), `UseCase` (a mesma forma `executar()` que os Use Cases de `application` já têm — nenhum precisou mudar) e `GerenciadorDeTransacao`.
- `pipeline.py` (`ImportadorPipeline`, genérica em `TEntrada`/`TSaida`) orquestra: valida o arquivo → lê em streaming (`yield`, nunca carrega tudo em memória) → mapeia → executa o Use Case → confirma a transação da linha → registra sucesso ou erro. Uma linha ruim (Value Object inválido, FK não resolvida, coluna faltando) nunca derruba as linhas seguintes — vira um `ErroImportacao` rastreável no `ResultadoImportacao` final, não uma exceção que aborta o lote inteiro.
- `readers/` (`CsvReader`, `ExcelReader`) implementam `Reader`; `factory.py` escolhe qual usar pela extensão do arquivo.
- `mappers/` (um por entidade) convertem linha crua em DTO — podem resolver FK por um identificador amigável (ex.: `inep` em vez de `escola_id`), mas nunca validam regra de negócio (isso é dos Value Objects, disparado quando o Use Case constrói a entidade).

### `exporters/`

`excel_exporter.py` existe como arquivo vazio — placeholder para "Exportação para Excel", item não iniciado em "Futuras Funcionalidades" do ROADMAP.

## Camada: Apresentation

Única camada que importa Flask. `app.py` expõe `criar_app(caminho_banco) -> Flask`, uma app factory (não um `app = Flask(...)` global) — o que permite criar quantas instâncias forem precisas (produção vs. cada teste com seu próprio banco `:memory:`).

**Ciclo de vida por requisição** é o detalhe mais importante desta camada:

```python
@app.before_request
def _abrir_container() -> None:
    if request.blueprint == "documentacao":
        return  # /docs e /openapi.yaml não tocam no banco
    g.container = Container(caminho_banco)

@app.teardown_appcontext
def _fechar_container(excecao: BaseException | None) -> None:
    container = g.pop("container", None)
    if container is not None:
        container.finalizar(sucesso=excecao is None)
```

Um `Container` **novo por requisição HTTP**, guardado em `flask.g`, fechado no teardown — nunca um Container global compartilhado entre requisições concorrentes. `teardown_appcontext` roda mesmo quando um error handler já converteu a exceção numa resposta JSON limpa (Flask propaga a exceção original até aqui de qualquer forma), garantindo que uma requisição que falhou sempre sofra rollback, mesmo que o cliente tenha recebido um 404/409/400 arrumadinho em vez de um 500.

**Controllers** (`apresentation/controllers/`) são funções soltas (não classes) — extraem o JSON do request, montam um DTO de `application`, chamam `g.container.<caso_de_uso>().executar(dto)`, serializam a saída. Não fazem tratamento de exceção (isso é global, em `erros.py`) nem chamam o repositório diretamente (sempre por um Use Case).

**Routes** (`apresentation/routes/`) são só `Blueprint` + `add_url_rule` — nenhuma lógica, só mapeamento HTTP → função do controller.

**`erros.py`** registra um `errorhandler` por família de exceção (`DomainError` → 400, `RegistroNaoEncontradoError` → 404, os 7 erros de "possui dependentes" → 409 mesmo herdando de `InfrastructureError`, etc. — tabela completa no `API.md`). Um único registro global; nenhum controller tem `try/except`.

**`serializacao.py`** converte um DTO (dataclass) em `dict` pronto para `jsonify`, existe porque `json.dumps` sozinho não serializa `datetime`.

**`documentacao.py`** serve `openapi.yaml` (escrito à mão, 40 operações / 26 schemas) cru em `/openapi.yaml` e via Swagger UI (CDN, sem dependência Python de parsing YAML) em `/docs`.

## Shared

Atravessa todas as camadas.

**`shared/exceptions/`** — hierarquia com 3 raízes (`DomainError`, `ApplicationError`, `InfrastructureError`), cada uma em seu próprio arquivo (`domain.py`, `application.py`, `infrastructure.py`) por origem: violação de Value Object, erro de coordenação entre entidades/repositórios, e falha de infraestrutura, respectivamente. `erros.py` (camada de apresentation) mapeia essas 3 famílias para status HTTP — ver `API.md` para a lista completa de exceções concretas.

**`shared/types/`** — um `NewType` por entidade (`EscolaId = NewType("EscolaId", int)`, etc.). Existe só para o type checker: em runtime é um `int` puro, sem custo, mas o mypy rejeita passar um `DreId` onde se espera um `EscolaId`, mesmo os dois sendo `int` por baixo.

## Fluxo de uma requisição, ponta a ponta

Trace completo de `POST /escolas` (o mesmo exemplo usado no `API.md`), atravessando as 4 camadas:

1. **Flask** roteia pro Blueprint de `apresentation/routes/escola_routes.py`, que aponta pra `criar_escola` em `apresentation/controllers/escola_controller.py`.
2. **Controller** lê `request.get_json(silent=True)`, confere campos obrigatórios, monta um `CriarEscolaInput` (dataclass de `application`) e chama `g.container.criar_escola().executar(dados)`.
3. **`g.container`** (um `Container`, aberto no `before_request` daquela requisição) monta a dependência: `EscolaModulo.criar_escola()` retorna `CriarEscolaUseCase(self.escola_repo())`, e `escola_repo()` instancia `SqliteEscolaRepository(self._conexao)` — a mesma conexão SQLite aberta pra essa requisição.
4. **Use Case** (`application/use_cases/escola/criar_escola.py`) constrói uma entidade `Escola` de `domain` — é aqui que `Inep(dados.inep)`, `Nome(dados.nome)`, `TipoEscola(dados.tipo)`, `Municipio(dados.municipio)`, `Endereco(...)` validam e normalizam. Um valor inválido levanta a exceção de domínio *antes* de qualquer SQL rodar.
5. Use Case chama `self._repositorio.salvar(escola)` — a interface `EscolaRepository` de `domain`, satisfeita em runtime por `SqliteEscolaRepository`.
6. **Repositório** roda o `INSERT`, captura `sqlite3.IntegrityError` se houver (INEP duplicado → `InepJaCadastradoError`; `dre_id` inexistente → `DreNaoEncontradaError`), preenche o `id` gerado na própria entidade e a devolve — **sem comitar**.
7. Use Case monta um `EscolaOutput` (DTO) a partir da entidade e devolve pro controller.
8. **Controller** chama `dto_para_dict(saida)` (`apresentation/serializacao.py`) e `jsonify(...)`, `201`.
9. Se tudo correu bem, `teardown_appcontext` chama `container.finalizar(sucesso=True)` → commit e fecha a conexão. Se qualquer passo acima tivesse levantado uma exceção, um `errorhandler` de `erros.py` já teria formatado a resposta de erro, e o mesmo teardown chamaria `finalizar(sucesso=False)` → rollback.

Nenhuma camada interna (domain, application) sabe que existe HTTP, Flask ou SQLite — só `apresentation` conhece Flask, só `infrastructure` conhece SQLite. É essa separação que permite os scripts de importação (próxima seção) reusarem exatamente os mesmos Use Cases sem tocar num só arquivo dessas duas camadas.

## `scripts/` — o outro ponto de entrada

Além da API HTTP, o projeto tem um segundo modo de escrever no banco: os importadores CLI (`scripts/importar_*.py`, um por entidade, mais `importar_tudo.py` que roda os 8 na ordem de dependência: DRE → Escola → {Diretor, CEMEP, Chromebook, Starlink} → Responsável → Turma).

Diferença-chave em relação à API: scripts **não usam `Container`**. Eles montam repositório e Use Case diretamente e usam `GerenciadorDeTransacaoSqlite` para confirmar **linha a linha** (não a importação inteira de uma vez) — assim uma linha 4.000 com erro não desfaz as 3.999 anteriores que já eram válidas. É a mesma razão pela qual `Container.finalizar()` (que comita a *requisição inteira*) não serviria aqui: API e importação têm granularidades de transação diferentes por natureza, então cada uma ganhou seu próprio mecanismo em vez de forçar um `transacao()` genérico único.

## Como os testes espelham a arquitetura

```
tests/
├── dominio/          # entidades + value objects — domain, isolado
├── application/       # casos de uso "buscar por relação" (cobertura parcial — ver observação abaixo)
├── infraestrutura/    # repositórios SQLite + Container, banco real (:memory:)
├── test_importacao/    # readers, mappers, pipeline, script de orquestração
├── test_interface/     # rotas HTTP fim-a-fim, erros.py, serializacao.py, documentacao.py
├── factories/          # test data builders (DreFactory, EscolaFactory...) — 1 por entidade
├── test_factories/     # testes QUE VALIDAM as factories acima (nome parecido, propósito diferente)
└── conftest.py          # fixtures compartilhadas: entidade pronta + repositório com create_autospec
```

284 testes no total. A maior parte do CRUD (criar/atualizar/remover/listar) é validada indiretamente pelas 65 rotas de `test_interface/` (fim-a-fim, batendo na API real) em vez de testes unitários dedicados por Use Case — só os casos de uso "buscar por relação" têm teste unitário próprio em `tests/application/`. `tests/infraestrutura/` é quem valida os repositórios contra um SQLite real, não um dublê — é ali que uma regressão de SQL ou de tradução de exceção apareceria.

## Decisões de design — os porquês

Uma seleção das decisões mais não-óbvias, todas documentadas no próprio código-fonte:

- **Tradução de exceção por código, não por texto.** `eh_violacao_unique`/`eh_violacao_foreign_key` (`infrastructure/database/sqlite/_util.py`) comparam `exc.sqlite_errorname`, não a mensagem do SQLite — a mensagem muda de idioma conforme o locale da máquina. Isso já foi bug uma vez (comparação de texto em português contra mensagem do SQLite em inglês, registrada no ROADMAP), corrigido ao trocar pra comparação de código de erro.
- **Container por requisição, não global.** A conexão usa `check_same_thread=False` (permite usar fora da thread que criou), mas isso não torna o objeto seguro pra uso *concorrente* — um Container global reaproveitado entre requisições paralelas correria esse risco. Os scripts CLI, que rodam sequencialmente, não têm esse problema e por isso não usam Container.
- **`Protocol` em vez de `ABC` no pipeline de importação.** Nenhuma implementação concreta (`CsvReader`, `EscolaMapper`, os próprios Use Cases de `application`) precisa herdar de nada — só ter o método certo. É isso que permite ao pipeline reusar `CriarEscolaUseCase` tal como já existia, sem tocar num arquivo da camada de aplicação para "encaixá-lo" numa interface nova.
- **Container como mixin.** `Container` herda de 8 `*Modulo` (um por entidade) em vez de compor um dicionário de dependências ou usar uma lib de DI. Cada módulo só sabe montar seu próprio repositório + Use Cases a partir de `self._conexao` (definida em `BaseModulo`); o `Container` final é a soma de todos.
- **Campos imutáveis via ausência de setter, não validação em runtime.** `Escola` não tem `alterar_inep`/`alterar_tipo`/`alterar_municipio` — não existe caminho de código para mudá-los depois de criados, então não há necessidade de checar "isso pode mudar?" a cada update.
- **`transacao.py` sem chamador ativo.** O context manager original (`with transacao(...) as conexao`) foi a primeira tentativa de padronizar commit/rollback, mas API (transação por requisição) e importação (transação por linha) precisavam de granularidades diferentes — cada uma ganhou seu próprio mecanismo (`Container.finalizar()` e `GerenciadorDeTransacaoSqlite`) e o arquivo original ficou no projeto sem uso. Não é um bug — é histórico de refatoração registrado no ROADMAP.

## Pontos de atenção conhecidos

Coisas que valem a pena saber ao navegar o código, para não estranhar:

- **O README.md tem um diagrama de pastas desatualizado** — mostra `domain/exceptions/` e `domain/factories/` (não existem; exceções ficam em `shared/exceptions/`, e não há factories de domínio) e `infrastructure/repositories/`/`infrastructure/schemas/` (na real estrutura ficam aninhados em `infrastructure/database/sqlite/`). Também não menciona a camada `apresentation/` nem `infrastructure/importacao/`, prováveis por terem sido escritas antes das Fases 4 e 5. Este documento reflete a estrutura real.
- **A camada `apresentation/` já foi chamada de `interface`.** A pasta de testes (`tests/test_interface/`) e o `openapi.yaml` (comentários e algumas descrições) ainda usam o nome antigo em alguns lugares — cosmético, não afeta comportamento.
- **`domain/enums/status_escola_projeto.py`** define `StatusEscolaProjeto` (`ATIVO`/`INATIVO`/`PENDENTE`), mas nenhuma entidade o usa e nenhuma rota o expõe — não faz parte da API hoje.
- **Casos de uso de busca por relação** (`buscar_diretor_por_escola`, `buscar_cemep_por_escola`, `buscar_chromebook_por_escola`, `buscar_escolas_por_dre`) existem e são testados, mas nenhum Container os expõe e nenhuma rota os chama — código pronto pra uma futura Fase que ainda não chegou.

---

*Gerado a partir da leitura do código-fonte em 25/08/2026.*
