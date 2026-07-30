# Arquitetura de Importação — `ImportadorPipeline`

Infraestrutura genérica de importação em lote que implementa a Fase 4
do roadmap (Importação Inicial) para as 8 entidades do domínio: DRE,
Escola, Diretor, CEMEP, Chromebook, Responsável, Turma CEMEP e
Starlink.

O algoritmo de importação — ler, mapear, executar, capturar erro,
reporta progresso, agrega resultado — **existe uma única vez**, em
`importacao/pipeline.py`. Cada entidade fornece apenas três peças:
um `Reader`, um `Mapper` e um `UseCase` já existente na camada de
aplicação. Nada de regra de negócio — isso continua
exclusivamente nos Value Objects e nos Use Cases.

Todo código citado abaixo é real, está no repositório e passa em
191 testes automatizados (49 deles cobrindo especificamente este
módulo).

---

## 1. Estrutura completa de pastas

```
importacao/                        # infraestrutura de importação
├── __init__.py                    # exports públicos do pacote
├── protocolos.py                  # Protocols: Reader, Mapper, UseCase
├── pipeline.py                    # ImportadorPipeline + ArquivoInvalidoError
├── resultado.py                   # ResultadoImportacao[TSaida]
├── erro.py                        # ErroImportacao (rico)
├── progresso.py                   # ProgressTracker + implementações
├── log_alteracao.py               # LogAlteracao, MudancaCampo, RegistroAlteracao
├── conversores.py                 # conversores puros str -> int/bool/date
├── resolvedores.py                # resolver_escola_id, resolver_cemep_id (FK compartilhadas)
├── readers/
│   ├── __init__.py
│   └── csv_reader.py              # CsvReader (streaming via yield)
└── mappers/
    ├── __init__.py
    ├── dre_mapper.py
    ├── escola_mapper.py
    ├── diretor_mapper.py
    ├── cemep_mapper.py
    ├── chromebook_mapper.py
    ├── starlink_mapper.py
    ├── responsavel_mapper.py
    └── turma_cemep_mapper.py

scripts/                           # composição concreta por entidade (CLI)
├── importar_dres.py
├── importar_escolas.py
├── importar_diretores.py
├── importar_cemeps.py
├── importar_chromebooks.py
├── importar_starlinks.py
├── importar_responsaveis.py
└── importar_turmas_cemep.py

tests/test_importacao/             # testes do pacote importacao
├── conftest.py                    # fixtures em cadeia: conexão -> dre -> escola -> cemep
├── test_csv_reader.py             # 7 testes — Reader isolado
├── test_pipeline.py               # 7 testes — algoritmo isolado, com dublês
├── test_mappers.py                # 26 testes — os 8 Mappers, incluindo resolução de FK
└── test_scripts_integracao.py     # 9 testes — cada script fim-a-fim + 1 teste de cadeia completa

docs/
└── importacao.md                  # este documento
```

**Por que um pacote novo no nível raiz, e não dentro de
`infrastructure/`?** `importacao/` chama Use Cases (camada de
aplicação) da mesma forma que `interface/` (a futura API REST) e
`scripts/` já fazem — ele é um *driver*, não um detalhe de persistência.
Colocar isso dentro de `infrastructure/database/` misturaria "como
os dados chegam de fora" com "como os dados são guardados", que são
preocupações independentes (ver seção 18).

## 2. Responsabilidade de cada pasta

| Pasta/arquivo | Responsabilidade | O que NUNCA deve estar aqui |
|---|---|---|
| `importacao/protocolos.py` | Definir o *contrato* estrutural de Reader, Mapper e UseCase | Qualquer implementação concreta |
| `importacao/pipeline.py` | O algoritmo — streaming, captura de erro, progresso, agregação | Qualquer conhecimento de CSV, SQLite, INEP, DRE etc. |
| `importacao/resultado.py`, `erro.py` | Estruturas de dados que representam o resultado de uma importação | Lógica de negócio; são dataclasses "burras" |
| `importacao/progresso.py` | Como reportar progresso (console, silencioso, ou futuramente UI) | Lógica de importação |
| `importacao/log_alteracao.py` | Registrar o que mudou quando uma linha *atualiza* (não cria) um registro | Decidir *se* algo é create ou update — isso é do Use Case |
| `importacao/conversores.py` | Conversão de tipo primitivo (str → int/bool/date) | Validação de regra de negócio (isso é dos Value Objects) |
| `importacao/resolvedores.py` | Resolução de FK compartilhada por mais de um Mapper (escola_id, cemep_id) | Regra de negócio — só faz *busca*, nunca decide se um valor é válido |
| `importacao/readers/` | Implementações concretas de `Reader` — hoje só CSV | Parsing de tipo, validação de negócio |
| `importacao/mappers/` | Um arquivo por entidade: linha crua → DTO, incluindo resolução de FK própria daquela entidade | Chamar o Use Case, gravar no banco, imprimir progresso |
| `scripts/importar_*.py` | Composição: escolhe o Reader, o Mapper, o Repository e o UseCase concretos; ponto de entrada CLI | O algoritmo de loop em si — isso é 100% do Pipeline |

## 3. Protocols/Interfaces

`importacao/protocolos.py` — três Protocols, não ABCs:

```python
class Reader(Protocol):
    def ler(self) -> Iterator[LinhaBruta]: ...
    def total_estimado(self) -> int | None: ...
    def validar(self) -> list[str]: ...


class Mapper(Protocol[TSaida_co]):
    def mapear(self, linha: LinhaBruta) -> TSaida_co: ...


class UseCase(Protocol[TEntrada_contra, TSaida_co]):
    def executar(self, dados: TEntrada_contra) -> TSaida_co: ...
```

Note a variância explícita: `Mapper` só **produz** `TSaida_co`
(covariante); `UseCase` **consome** `TEntrada_contra`
(contravariante) e **produz** `TSaida_co` (covariante). Sem isso o
mypy rejeita os Protocols — a variância errada permitiria, em tese,
passar um `Mapper[Escola]` onde a assinatura promete aceitar
qualquer `Mapper[object]`, quebrando segurança de tipo silenciosamente.

**Por que Protocol e não ABC:** nenhuma classe concreta precisa herdar
de nada. `CriarEscolaUseCase` já satisfaz `UseCase[CriarEscolaInput,
EscolaOutput]` exatamente como foi escrito antes deste desenho
existir — zero linhas alteradas na camada de aplicação. Isso é
subtyping estrutural (duck typing verificado estaticamente): o
Protocol descreve *forma*, não *linhagem*.

## 4. Classes principais

| Classe | Papel |
|---|---|
| `ImportadorPipeline[TEntrada, TSaida]` | Orquestra uma importação completa |
| `CsvReader` | Único `Reader` concreto hoje; sabe ler CSV em streaming |
| `DreMapper`, `EscolaMapper`, ... (8 classes) | Um `Mapper` por entidade |
| `ResultadoImportacao[TSaida]` | Agrega sucessos + erros de uma execução |
| `ErroImportacao` | Uma falha de linha, com contexto completo |
| `ProgressTrackerConsole` / `ProgressTrackerSilencioso` | Como o progresso é exibido (ou não, em teste) |
| `LogAlteracao` | Acumula mudanças de campo quando uma importação faz update |
| `ArquivoInvalidoError` | Levantada quando `Reader.validar()` reprova o arquivo antes da 1ª linha |

## 5. Fluxo completo de importação de uma Escola

`EscolaMapper` é o exemplo mais rico porque resolve uma FK por dois
caminhos (id direto ou nome), o mesmo padrão usado por Diretor, CEMEP,
Chromebook e Starlink (via `resolvedores.resolver_escola_id`):

```python
# importacao/mappers/escola_mapper.py
class EscolaMapper:
    COLUNAS_OBRIGATORIAS = ["inep", "nome", "tipo", "municipio"]

    def __init__(self, repo_dre: DreRepository) -> None:
        self._repo_dre = repo_dre

    def mapear(self, linha: dict[str, str]) -> CriarEscolaInput:
        return CriarEscolaInput(
            inep=linha["inep"].strip(),
            nome=linha["nome"].strip(),
            tipo=linha["tipo"].strip().upper(),
            municipio=linha["municipio"].strip(),
            dre_id=self._resolver_dre_id(linha),
            endereco=para_texto_opcional(linha.get("endereco")),
        )

    def _resolver_dre_id(self, linha: dict[str, str]) -> int:
        dre_id_bruto = (linha.get("dre_id") or "").strip()
        if dre_id_bruto:
            return int(dre_id_bruto)

        nome = (linha.get("dre_nome") or "").strip()
        if not nome:
            raise ValueError("Linha não informou nem dre_id nem dre_nome.")

        encontradas = self._repo_dre.buscar_por_nome(Nome(nome))
        if not encontradas:
            raise ValueError(f"DRE com nome '{nome}' não encontrada.")
        if len(encontradas) > 1:
            raise ValueError(f"Mais de uma DRE encontrada com o nome '{nome}'...")

        dre_id = encontradas[0].id
        if dre_id is None:
            raise ValueError(f"DRE com nome '{nome}' não possui id persistido.")
        return dre_id
```

E a composição inteira, em `scripts/importar_escolas.py`:

```python
def importar_escolas(caminho_csv, caminho_banco="escolas.db") -> ResultadoImportacao:
    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)

    repo_dre = SqliteDreRepository(conexao)
    repo_escola = SqliteEscolaRepository(conexao)

    pipeline = ImportadorPipeline(
        reader=CsvReader(caminho_csv, colunas_obrigatorias=EscolaMapper.COLUNAS_OBRIGATORIAS),
        mapper=EscolaMapper(repo_dre),
        use_case=CriarEscolaUseCase(repo_escola),
    )

    resultado = pipeline.executar()
    if resultado.erros:
        resultado.exportar_falhas_csv(caminho_falhas)
    conexao.close()
    return resultado
```

Passo a passo real, linha a linha de um CSV de escolas:

1. **Validação do arquivo** — `CsvReader.validar()` confere se `inep`,
   `nome`, `tipo`, `municipio` existem no cabeçalho. Se faltar uma,
   `ImportadorPipeline.executar()` levanta `ArquivoInvalidoError`
   **antes** de ler a primeira linha de dados.
2. **Reader (streaming)** — `CsvReader.ler()` produz um `dict` por vez
   via `csv.DictReader`, nunca uma lista completa.
3. **Mapper** — `EscolaMapper.mapear(linha)` resolve `dre_id` (direto
   ou via `dre_nome` → `DreRepository.buscar_por_nome`) e monta
   `CriarEscolaInput`.
4. **Use Case** — `CriarEscolaUseCase.executar(dto)`, **inalterado**,
   constrói `Inep`, `Nome`, `Municipio`, `TipoEscola`, `Endereco` (os
   Value Objects validam aqui) e chama `EscolaRepository.salvar`.
5. **Resultado** — sucesso vira `EscolaOutput` em
   `resultado.sucessos`; qualquer exceção em qualquer um dos passos
   2-4 vira um `ErroImportacao` em `resultado.erros`, e a próxima
   linha continua sendo processada.

## 6. Implementação do `ImportadorPipeline` genérico

Estrutura real e completa da lógica (docstrings internos e comentários
omitidos por brevidade — o arquivo integral está em
`importacao/pipeline.py`):

```python
TEntrada = TypeVar("TEntrada")
TSaida = TypeVar("TSaida")


class ArquivoInvalidoError(Exception):
    def __init__(self, problemas: list[str]) -> None:
        self.problemas = problemas
        super().__init__("; ".join(problemas))


class ImportadorPipeline(Generic[TEntrada, TSaida]):
    def __init__(
        self,
        reader: Reader,
        mapper: Mapper[TEntrada],
        use_case: UseCase[TEntrada, TSaida],
        progress_tracker: ProgressTracker | None = None,
        log_alteracao: LogAlteracao | None = None,
    ) -> None:
        self._reader = reader
        self._mapper = mapper
        self._use_case = use_case
        self._progress = progress_tracker or ProgressTrackerConsole()
        self.log_alteracao = log_alteracao

    def executar(self) -> ResultadoImportacao[TSaida]:
        problemas = self._reader.validar()
        if problemas:
            raise ArquivoInvalidoError(problemas)

        resultado: ResultadoImportacao[TSaida] = ResultadoImportacao()
        total = self._reader.total_estimado()

        processados = 0
        for linha in self._reader.ler():
            processados += 1
            try:
                dto = self._mapper.mapear(linha)
                saida = self._use_case.executar(dto)
                resultado.registrar_sucesso(saida)
            except Exception as excecao:
                erro = ErroImportacao.a_partir_de(processados, linha, excecao)
                resultado.registrar_erro(erro)
            self._progress.atualizar(processados, total)

        self._progress.finalizar(resultado)
        return resultado
```

Pontos que valem explicação:

- **`Generic[TEntrada, TSaida]` na classe, não só nos métodos** — é o
  que faz `TSaida` do `__init__` ser *o mesmo* `TSaida` do `executar`,
  para o type checker. Sem isso, `pipeline.executar()` não tem como
  inferir automaticamente que devolve `ResultadoImportacao[EscolaOutput]`
  quando você passou um `CriarEscolaUseCase` — cada script precisaria
  anotar manualmente. Foi um erro real que o mypy pegou durante a
  construção deste pacote (ver seção 18, "Eficiência do processo").
- **`except Exception` é deliberado, não descuido** — está documentado
  no próprio código. Uma linha ruim nunca pode derrubar as 49 mil
  seguintes; o erro não é engolido, vira um `ErroImportacao`
  rastreável. `KeyboardInterrupt`/`SystemExit` não são pegos por isso
  (herdam de `BaseException`, não de `Exception`).
- **`validar()` roda ANTES do loop** — decisão consciente de falhar
  rápido. Não faz sentido processar 50 mil linhas pra só então
  descobrir que faltava uma coluna inteira no cabeçalho.

## 7. Exemplo de processamento usando `yield`

`CsvReader.ler()` — a prova de que isso é streaming de verdade, não
só "parece" streaming:

```python
def ler(self) -> Iterator[dict[str, str]]:
    with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        yield from leitor
```

O arquivo só é aberto quando alguém começa a **iterar** o resultado
de `ler()` — chamar `ler()` sozinho não lê nada. Isso é testado
diretamente (`tests/test_importacao/test_csv_reader.py`):

```python
def test_ler_e_um_generator_nao_le_o_arquivo_na_hora_da_chamada(tmp_path):
    caminho_inexistente = tmp_path / "nao_existe.csv"
    gerador = CsvReader(caminho_inexistente).ler()
    assert inspect.isgenerator(gerador)   # não levantou FileNotFoundError
```

Se `.ler()` devolvesse `list(csv.DictReader(...))` — como o utilitário
antigo (`scripts/_importador_util.py`, removido) fazia — o Python já
teria lido e materializado o arquivo inteiro antes mesmo do Pipeline
processar a primeira linha. Com `yield`, cada linha existe na memória
só durante sua própria iteração do `for` em `pipeline.py`; o resto do
arquivo continua no disco.

## 8. Exemplo de Reader

`CsvReader` — estrutura completa da lógica, docstrings omitidos por
brevidade (arquivo integral em `importacao/readers/csv_reader.py`):

```python
class CsvReader:
    def __init__(self, caminho, colunas_obrigatorias=None, encoding="utf-8"):
        self._caminho = Path(caminho)
        self._colunas_obrigatorias = colunas_obrigatorias or []
        self._encoding = encoding

    def validar(self) -> list[str]:
        problemas = []
        if not self._caminho.exists():
            problemas.append(f"Arquivo não encontrado: {self._caminho}")
            return problemas

        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            colunas_presentes = set(leitor.fieldnames or [])

        faltando = [c for c in self._colunas_obrigatorias if c not in colunas_presentes]
        if faltando:
            problemas.append(f"Coluna(s) obrigatória(s) ausente(s): {', '.join(faltando)}")
        return problemas

    def ler(self) -> Iterator[dict[str, str]]:
        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            yield from csv.DictReader(arquivo)

    def total_estimado(self) -> int | None:
        if not self._caminho.exists():
            return None
        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            return max(sum(1 for _ in arquivo) - 1, 0)
```

`total_estimado()` conta linhas somando `1 for _ in arquivo` — O(n) em
tempo, mas **O(1) em memória**: nunca guarda o conteúdo, só incrementa
um contador. Serve exclusivamente para o `ProgressTracker` mostrar
"processado X de Y"; se não for possível saber (arquivo não existe),
devolve `None` e o progresso cai para "X linha(s)" sem percentual.

## 9. Exemplo de Mapper

O mais simples de todos, sem FK nenhuma — `DreMapper`:

```python
class DreMapper:
    COLUNAS_OBRIGATORIAS = ["nome"]

    def mapear(self, linha: dict[str, str]) -> CriarDreInput:
        return CriarDreInput(
            nome=linha["nome"].strip(),
            telefone=para_texto_opcional(linha.get("telefone")),
        )
```

E o `TurmaCemepMapper`, que ilustra um limite deliberado — nem todo
Mapper precisa (ou deve) resolver FK por nome:

```python
class TurmaCemepMapper:
    """
    Só aceito responsavel_id direto — de propósito. Resolver por nome
    exigiria encadear escola_inep -> escola_id -> cemep_id -> lista de
    responsáveis -> filtrar por nome em Python, sem garantia de nome
    único dentro do mesmo CEMEP: uma ambiguidade silenciosa que
    prefiro não introduzir.
    """
    COLUNAS_OBRIGATORIAS = ["nome_turma", "responsavel_id"]

    def mapear(self, linha: dict[str, str]) -> CriarTurmaCemepInput:
        return CriarTurmaCemepInput(
            responsavel_id=int(linha["responsavel_id"].strip()),
            nome_turma=linha["nome_turma"].strip(),
        )
```

## 10. Exemplo de DTO

Os DTOs **já existiam** na camada de aplicação, escritos na Fase 2 —
o Pipeline não define nenhum DTO novo, só os alimenta:

```python
# application/use_cases/escola/dtos.py — não foi tocado por este trabalho
@dataclass(frozen=True, slots=True)
class CriarEscolaInput:
    inep: str
    nome: str
    tipo: str
    municipio: str
    dre_id: int
    endereco: str | None = None
```

## 11. Exemplo de Use Case reutilizado

`CriarEscolaUseCase` — **zero linhas alteradas** desde a Fase 2:

```python
# application/use_cases/escola/criar_escola.py — inalterado.
# Trecho abaixo: corpo real da classe, com imports e docstrings
# (de módulo, classe e do método executar()) omitidos por brevidade —
# arquivo integral no caminho acima.
class CriarEscolaUseCase:
    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarEscolaInput) -> EscolaOutput:
        escola = Escola(
            id=None,
            inep=Inep(dados.inep),
            nome=Nome(dados.nome),
            tipo=TipoEscola(dados.tipo),
            municipio=Municipio(dados.municipio),
            dre_id=DreId(dados.dre_id),
            endereco=Endereco(dados.endereco) if dados.endereco else None,
        )

        escola_criada = self._repositorio.salvar(escola)

        if escola_criada.id is None:
            raise PersistenciaInconsistenteError("O repositório retornou uma Escola sem id.")

        return EscolaOutput(
            id=escola_criada.id,
            inep=escola_criada.inep.valor,
            nome=escola_criada.nome.valor,
            tipo=escola_criada.tipo.value,
            municipio=escola_criada.municipio.valor,
            dre_id=escola_criada.dre_id,
            endereco=escola_criada.endereco.valor if escola_criada.endereco else None,
            criado_em=escola_criada.criado_em,
            atualizado_em=escola_criada.atualizado_em,
        )
```

Isso satisfaz `UseCase[CriarEscolaInput, EscolaOutput]` só por ter o
método `executar` com essa forma — nenhuma herança, nenhum import de
`importacao` dentro da camada de aplicação.

## 12. Exemplo de `ResultadoImportacao`

```python
@dataclass
class ResultadoImportacao(Generic[TSaida]):
    sucessos: list[TSaida] = field(default_factory=list)
    erros: list[ErroImportacao] = field(default_factory=list)

    def registrar_sucesso(self, saida: TSaida) -> None:
        self.sucessos.append(saida)

    def registrar_erro(self, erro: ErroImportacao) -> None:
        self.erros.append(erro)

    @property
    def taxa_sucesso(self) -> float:
        total = len(self.sucessos) + len(self.erros)
        return len(self.sucessos) / total if total else 0.0

    def resumo(self) -> str:
        return (f"{len(self.sucessos)} registro(s) importado(s) com sucesso, "
                f"{len(self.erros)} falha(s) ({self.taxa_sucesso:.1%} de sucesso).")

    def exportar_falhas_csv(self, caminho) -> None:
        if not self.erros:
            return
        colunas = list(self.erros[0].dados_originais.keys()) + ["numero_linha", "tipo_erro", "motivo"]
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()
            for erro in self.erros:
                escritor.writerow(erro.linha_relatorio())
```

`exportar_falhas_csv` grava no **mesmo formato de entrada** (colunas
originais primeiro) mais três colunas de diagnóstico — o CSV de
falhas pode ser corrigido em planilha e apontado de volta pro mesmo
script, viabilizando "reimportação apenas das linhas com erro" sem
nenhum código extra: é só rodar `python -m scripts.importar_escolas
escolas_falhas.csv` depois de corrigir.

## 13. Exemplo de `ErroImportacao` rico

```python
@dataclass(frozen=True)
class ErroImportacao:
    numero_linha: int
    dados_originais: dict[str, str]
    tipo_erro: str
    mensagem: str
    campo: str | None = None
    ocorrido_em: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def a_partir_de(cls, numero_linha, dados_originais, excecao: Exception):
        return cls(
            numero_linha=numero_linha,
            dados_originais=dict(dados_originais),
            tipo_erro=type(excecao).__name__,
            mensagem=str(excecao),
            campo=getattr(excecao, "campo", None),
        )
```

"Rico" aqui significa: qualquer pessoa consegue corrigir a linha só
lendo o CSV de falhas, sem abrir o código-fonte — tem a linha exata
(`numero_linha`), os dados exatos que foram tentados
(`dados_originais`), o tipo de erro pra filtrar/agrupar (`tipo_erro` —
ex. `EscolaJaPossuiDiretorError`) e a mensagem legível (`mensagem`).
`campo` é *best effort*: só populado se a exceção específica expuser
esse atributo — nenhuma exceção de domínio hoje expõe, então fica
`None` na prática; o design já suporta se um dia alguma passar a
expor.

## 14. Exemplo de `ProgressTracker`

```python
class ProgressTracker(Protocol):
    def atualizar(self, processados: int, total: int | None) -> None: ...
    def finalizar(self, resultado: ResultadoImportacao) -> None: ...


class ProgressTrackerConsole:
    def __init__(self, intervalo: int = 500) -> None:
        self._intervalo = intervalo

    def atualizar(self, processados, total) -> None:
        if processados % self._intervalo != 0:
            return
        if total:
            print(f"\r  processando... {processados}/{total} ({processados/total:.1%})",
                  end="", file=sys.stderr)
        else:
            print(f"\r  processando... {processados} linha(s)", end="", file=sys.stderr)

    def finalizar(self, resultado) -> None:
        print(file=sys.stderr)
        print(resultado.resumo())
```

Imprime a cada 500 linhas (não a cada linha — um arquivo de 200 mil
linhas não deveria gerar 200 mil `print`s) e em `stderr` (não polui
uma saída que porventura seja redirecionada/parseada). Existe também
`ProgressTrackerSilencioso`, usado pelos 49 testes deste pacote — sem
ele, rodar a suíte imprimiria barra de progresso de cada teste.

## 15. Exemplo de `LogAlteracao`

```python
class LogAlteracao:
    def __init__(self) -> None:
        self._registros: list[RegistroAlteracao] = []

    def registrar(self, entidade: str, identificador: int, mudancas: list[MudancaCampo]) -> None:
        if not mudancas:
            return
        self._registros.append(RegistroAlteracao(entidade, identificador, mudancas))

    def exportar_csv(self, caminho) -> None:
        ...  # entidade, id, campo, valor_antigo, valor_novo, ocorrido_em
```

**Estado atual, com honestidade**: `ImportadorPipeline` aceita
`log_alteracao` no construtor e o expõe depois de `.executar()` via
`pipeline.log_alteracao`, mas **nenhum Mapper ou Use Case de hoje o
alimenta** — a Fase 4 do roadmap é só criação ("Importação Inicial"),
nenhum dos 8 Use Cases de `Criar*` faz upsert. A peça está pronta e
testável isoladamente; o dia em que existir reimportação incremental
(atualizar em vez de duplicar), um futuro `AtualizarOuCriarXUseCase`
passaria a chamar `log.registrar(...)` a cada campo que mudou. Incluí
porque foi pedido explicitamente e porque não atrapalha nada estando
pronto e ocioso — mas seria enganoso dizer que já está "em uso".

## 16. Como desacoplar CSV para suportar Excel futuramente

Nenhuma peça fora de `importacao/readers/csv_reader.py` importa o
módulo `csv`. O Pipeline depende só do Protocol `Reader`; os Mappers
recebem `dict[str, str]` e nunca sabem de onde ele veio. Adicionar
Excel é escrever **uma classe nova**, sem tocar em Pipeline, Mapper,
UseCase ou nos scripts de composição — só troca qual `Reader` é
passado:

```python
# esboço — precisaria de `pip install openpyxl`, ainda não adicionado
# ao requirements.txt (o projeto hoje é stdlib-only de propósito)
from openpyxl import load_workbook

class ExcelReader:
    def __init__(self, caminho, aba: str | None = None, colunas_obrigatorias=None):
        self._caminho = caminho
        self._aba = aba
        self._colunas_obrigatorias = colunas_obrigatorias or []

    def validar(self) -> list[str]:
        # abrir em read_only=True, checar a linha de cabeçalho,
        # comparar com colunas_obrigatorias — mesma lógica do CsvReader
        ...

    def ler(self) -> Iterator[dict[str, str]]:
        workbook = load_workbook(self._caminho, read_only=True)
        planilha = workbook[self._aba] if self._aba else workbook.active
        linhas = planilha.iter_rows(values_only=True)
        cabecalho = next(linhas)
        for linha in linhas:
            yield {coluna: str(valor) if valor is not None else "" for coluna, valor in zip(cabecalho, linha)}
        workbook.close()

    def total_estimado(self) -> int | None:
        workbook = load_workbook(self._caminho, read_only=True)
        total = workbook.active.max_row - 1
        workbook.close()
        return total
```

`load_workbook(..., read_only=True)` do openpyxl já é *streaming* por
baixo dos panos (não carrega a planilha inteira), então a propriedade
"nunca materializar o arquivo inteiro em memória" se mantém.

Uso, depois de existir: `scripts/importar_escolas.py` passaria a
aceitar tanto `.csv` quanto `.xlsx` só decidindo qual Reader
instanciar pela extensão do arquivo — **nenhuma outra linha do
projeto mudaria**:

```python
reader = ExcelReader(caminho) if caminho.suffix == ".xlsx" else CsvReader(caminho)
pipeline = ImportadorPipeline(reader=reader, mapper=EscolaMapper(repo_dre), use_case=...)
```

O mesmo raciocínio vale para Google Sheets (um `GoogleSheetsReader`
usando a API do Sheets, paginando em vez de ler tudo de uma vez) ou
uma API REST de terceiro (um `ApiReader` paginando requisições) — todos
só precisam produzir `Iterator[dict[str, str]]`.

**Nota**: este esboço não foi adicionado ao projeto como arquivo real
nem testado — o pedido foi "como desacoplar", não "adicionar suporte
a Excel agora". Se quiser isso implementado de verdade, é só pedir;
envolve adicionar `openpyxl` a `requirements.txt`, que hoje é
deliberadamente stdlib-only.

## 17. Padrões de projeto utilizados, e por quê

| Padrão | Onde | Por quê |
|---|---|---|
| **Strategy** | `Reader`, `Mapper`, `UseCase`, `ProgressTracker` são estratégias intercambiáveis injetadas no `ImportadorPipeline` | É o padrão central do desenho. Permite trocar CSV por Excel, ou um `ProgressTrackerConsole` por um silencioso, sem tocar no algoritmo. Preferido sobre Template Method (que exigiria subclassificar o Pipeline pra cada entidade) porque composição > herança: 8 entidades por herança seriam 8 subclasses acopladas à implementação da classe-mãe; por composição, são 8 objetos independentes, testáveis isoladamente |
| **Adapter** | `CsvReader` adapta a API do módulo `csv` para o Protocol `Reader`; um futuro `ExcelReader` adaptaria `openpyxl` do mesmo jeito | Isola o Pipeline de qualquer biblioteca externa específica — troca de biblioteca de leitura nunca se propaga |
| **Iterator** | `Reader.ler() -> Iterator[LinhaBruta]`, implementado com `yield` | É o que viabiliza streaming sem estruturas de dados customizadas — usa o protocolo de iteração nativo do Python |
| **Repository** | `DreRepository`, `EscolaRepository` etc. (já existiam) — os Mappers e `resolvedores.py` dependem das *interfaces* (`domain.repositories`), nunca de `SqliteXRepository` | Um Mapper não sabe (nem pode saber) que o banco é SQLite. Ver seção 18 |
| **DTO (Data Transfer Object)** | `CriarEscolaInput` e os outros 7 (já existiam) | Fronteira estável entre "o que chega de fora" e "o que o domínio entende" — o Mapper produz DTO, nunca uma Entidade diretamente |
| **Dependency Injection (via construtor)** | `ImportadorPipeline(reader=..., mapper=..., use_case=...)`; cada Mapper recebe seus Repositories no `__init__` | Testabilidade: `test_pipeline.py` usa dublês de Reader/Mapper/UseCase sem nenhum framework de DI, só passando outro objeto no mesmo parâmetro |
| **Notification / Collecting Parameter** (Fowler) | `ResultadoImportacao` acumula sucessos e `ErroImportacao` em vez de lançar excend~co na primeira falha | É o mecanismo formal por trás de "continuar processando após erros" — a alternativa (lançar na 1ª falha) é incompatível com processar um arquivo de 500 mil linhas onde 40 têm problema |
| **Pipeline / Pipes-and-Filters** | O próprio `ImportadorPipeline.executar()`: validação → leitura → mapeamento → execução → agregação, em estágios discretos | Dá nome ao desenho geral: cada estágio faz uma coisa e passa pro próximo; fica óbvo onde adicionar um estágio novo (ex.: um estágio de deduplicação, se um dia for preciso) |
| **Protocol / Structural typing** | Toda a camada de contratos (`protocolos.py`) usa `typing.Protocol`, não `abc.ABC` | Não é um padrão GoF clássico, mas é a decisão arquitetural mais consequente do pacote: permite reusar os 8 `CriarXUseCase` sem alterar uma linha deles. Ver seção 18 |

## 18. Justificativa arquitetural

**DDD.** Nenhuma regra de negócio existe em `importacao/`. `Nome`,
`Inep`, `Municipio`, `Quantidade`, `TipoEscola` continuam sendo a
única fonte de verdade sobre o que é um dado válido — o Mapper monta
um DTO com dados *brutos* (`linha["nome"].strip()`), e é o Use Case,
chamando o Value Object, quem decide se aquilo é aceitável. Um
exemplo concreto: `ChromebookMapper` converte `"30"` → `30` (tipo),
mas não decide se 30 é uma quantidade válida — isso é
`Quantidade.__post_init__` verificando `> 0`. Se essa regra migrasse
pro Mapper, o mesmo conhecimento existiria em dois lugares, e um dia
os dois divergiriam — o mesmo tipo de problema que motivou, mais
cedo neste projeto, a correção de `eh_violacao_unique`/
`eh_violacao_foreign_key`: duas fontes de verdade para o mesmo fato
acabam desincronizando.

**Clean Architecture (regra de dependência).** `importacao/` importa
de `domain` e `application`; nem `domain` nem `application` sabem
que `importacao` existe. `EscolaMapper` depende de `DreRepository`
(a interface, em `domain.repositories`), nunca de
`SqliteDreRepository` — quem decide *qual* implementação injetar é
o script de composição (`scripts/importar_escolas.py`), exatamente
como o próprio comentário de `infrastructure/database/__init__.py`
já documentava antes deste trabalho ("é o código de composição
[...] que decide qual implementação injetar em cada Use Case"). Os
Protocols em `protocolos.py` são as *portas* (no sentido de
ports-and-adapters); `CsvReader` é um *adaptador* concreto de uma
delas. Trocar SQLite por Postgres no futuro não tocaria uma linha de
`importacao/` — só a pasta `infrastructure/database/`.

**Eficiência.** Streaming via `yield` mantém uso de memória O(1) em
relação ao tamanho do arquivo — testado explicitamente
(`test_ler_e_um_generator_...`). `total_estimado()` é O(n) em tempo
mas O(1) em memória (soma linhas, não guarda conteúdo). O mypy, ao
ser rodado sobre este pacote, pegou um erro real de generics mal
propagados (`ImportadorPipeline` não declarado `Generic[...]`
corretamente) que fazia cada script precisar de anotação de tipo
manual — corrigido na própria raiz (a classe passou a herdar de
`Generic[TEntrada, TSaida]`), então o benefício se propagou pros 8
scripts sem tocar em nenhum deles individualmente. É o mesmo
princípio de "um lugar só pra cada verdade" aplicado à tipagem, não
só à lógica de negócio.

**Escalabilidade.** O algoritmo não muda entre um CSV de 10 linhas e
um de 500 mil (todas as escolas do Pará). Adicionar uma 9ª entidade no
futuro significa escrever um Mapper novo (~20-40 linhas, seguindo o
padrão de `DreMapper` ou `EscolaMapper`) e um script de composição —
zero mudança em `pipeline.py`, `resultado.py`, `erro.py` ou
`progresso.py`. Adicionar uma fonte nova (Excel, Sheets, API) é
simetricamente o mesmo: um Reader novo, zero mudança em Mapper/UseCase.

**Baixo acoplamento.** Nenhum Mapper conhece SQLite. Nenhum Reader
conhece DRE, Escola ou qualquer conceito de domínio. O Pipeline não
conhece nenhum dos dois. Essa separação é o que permitiu testar as 3
camadas de forma independente: `test_pipeline.py` (7 testes) usa
dublês falsos — nem SQLite nem CSV real entram nesses testes;
`test_csv_reader.py` (7 testes) testa leitura sem nenhuma entidade de
domínio; `test_mappers.py` (26 testes) testa resolução de FK com
banco real, mas sem nunca instanciar um `ImportadorPipeline`. Cada
camada quebra (ou não) por razões que só pertencem a ela.

**Facilidade de manutenção.** Bug em como se reporta progresso? Um
lugar (`progresso.py`), efeito em 8 entidades. Bug em como se decide
que uma linha falhou? Um lugar (`pipeline.py`), mesmo efeito. Isso já
se provou na prática dentro deste mesmo projeto: a correção de
`eh_violacao_unique`/`eh_violacao_foreign_key` (de comparação de texto
em português para `sqlite_errorname`) feita num só arquivo
corrigiu simultaneamente o comportamento de erro de Escola, Diretor,
CEMEP e Chromebook — o mesmo princípio de "consolidar antes de
replicar" que motivou este pacote inteiro em vez de continuar copiando
a mesma função de importação 8 vezes.
