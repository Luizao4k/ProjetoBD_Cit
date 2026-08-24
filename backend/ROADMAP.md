# 🗺️ Roadmap

Sistema para gerenciamento de dados da CIT sobre escolas do Estado do Pará.

Projeto desenvolvido para estudo de **Python**, **Domain-Driven Design (DDD)** e
**Clean Architecture**, evoluindo gradualmente até uma aplicação pronta para
produção.

---

# Status Geral

| Etapa | Status |
|--------|--------|
| Domínio | ✅ |
| Aplicação | ✅ |
| Infraestrutura | ✅ |
| Importação Inicial | ✅ |
| API REST | ✅ |
| Segurança | ⬜ |
| Banco de Produção | ⬜ |
| Qualidade | ⬜ |
| Deploy | ⬜ |

---

# Fase 1 — Domínio ✅

Objetivo: modelar corretamente as regras de negócio.

## Entidades

- [x] DRE
- [x] Escola
- [x] Diretor
- [x] CEMEP
- [x] Responsável
- [x] Turma CEMEP
- [x] Chromebook
- [x] Starlink

## Value Objects

- [x] Nome
- [x] Email
- [x] Telefone
- [x] Município
- [x] Endereço
- [x] Quantidade
- [x] Comentário

## Outros

- [x] Repositórios (interfaces)
- [x] IDs tipados
- [x] Enums
- [x] Exceções de domínio

---

# Fase 2 — Aplicação ✅

Objetivo: implementar os casos de uso.

## Casos de Uso

- [x] CRUD de DRE
- [x] CRUD de Escola
- [x] CRUD de Diretor
- [x] CRUD de CEMEP
- [x] CRUD de Chromebook
- [x] CRUD de Responsável
- [x] CRUD de Turma
- [x] CRUD de Starlink

## DTOs

- [x] Input DTOs
- [x] Output DTOs

## Exceções

- [x] Registro não encontrado
- [x] Registro duplicado
- [x] Relação inexistente

---

# Fase 3 — Infraestrutura ✅

Objetivo: conectar a aplicação ao banco de dados.

## Banco

- [x] SQLite
- [x] Connection Factory
- [x] Schema separado

## Repositórios SQLite

- [x] DRE
- [x] Escola
- [x] Diretor
- [x] CEMEP
- [x] Chromebook
- [x] Responsável
- [x] Turma
- [x] Starlink

## Container

- [x] Base Module
- [x] DRE Module
- [x] Escola Module
- [x] Diretor Module
- [x] CEMEP Module
- [x] Chromebook Module
- [x] Responsável Module
- [x] Turma Module
- [x] Starlink Module

## Infraestrutura

- [x] Tradução de exceções SQLite
- [x] Padronização dos repositórios
- [x] Padronização do ciclo de conexão

## Testes

- [x] Testes dos repositórios
- [x] Testes de integração

**Nota:** dois bugs que impediam a suíte inteira de rodar (import
trocado em `infrastructure/database/sqlite/__init__.py`; detecção de
violação de integridade comparando texto em português contra
mensagens do SQLite, que vêm em inglês) foram corrigidos. Os 284
testes do projeto passam hoje.

Os repositórios pararam de comitar sozinhos a cada escrita — quem
decide quando confirmar é o chamador: `Container.finalizar()` pra
requisições da API (um Container por requisição), e
`GerenciadorDeTransacaoSqlite` pra cada linha de uma importação (Fase
4). O `transacao()` original de `transacao.py` acabou não sendo o
mecanismo usado — API e importação precisavam de granularidades
diferentes (uma requisição inteira vs. uma linha por vez), então cada
uma ganhou sua própria implementação em vez de um único `with
transacao(...)` genérico. `transacao.py` segue no projeto sem
nenhum chamador. Ver "Melhorias Arquiteturais".

---

# Fase 4 — Importação Inicial ✅

## Leitura

- [x] Leitor CSV
- [x] Leitor Excel
- [x] Normalização dos dados
- [x] Conversão para DTOs

## Importadores

- [x] DRE
- [x] Escola
- [x] Diretor
- [x] CEMEP
- [x] Chromebook
- [x] Responsável
- [x] Turma
- [x] Starlink

## Orquestração

- [x] Ordem correta de importação
- [x] Registro de erros
- [x] Relatório final
- [x] Reimportação das linhas com erro

Implementado como um `ImportadorPipeline` genérico (Strategy +
Protocol, streaming via `yield`) reutilizado pelas 8 entidades — ver
`docs/backend/importacao.md` para a arquitetura completa. `ExcelReader`
implementa o mesmo Protocol `Reader` que `CsvReader`; qual dos dois
usar é decidido por `criar_reader()` (extensão do arquivo), então
nenhum script precisa saber se está lendo CSV ou Excel.
`scripts/importar_tudo.py` roda os 8 importadores num único comando,
na ordem de dependência (DRE → Escola → {Diretor, CEMEP, Chromebook,
Starlink} → Responsável → Turma), pulando com aviso qualquer entidade
sem arquivo em vez de falhar o lote inteiro. 284 testes automatizados
cobrem o projeto hoje, 74 deles este módulo.

---

# Fase 5 — API REST ✅

Objetivo: disponibilizar os casos de uso via HTTP.

## Estrutura

- [x] Flask
- [x] Blueprints
- [x] Configurações
- [x] Injeção de dependências

## Controllers

- [x] DRE
- [x] Escola
- [x] Diretor
- [x] CEMEP
- [x] Chromebook
- [x] Responsável
- [x] Turma
- [x] Starlink

## API

- [x] CRUD completo
- [x] Tratamento global de exceções
- [x] Serialização dos DTOs
- [x] Documentação OpenAPI

Um `Container` novo por requisição HTTP (`flask.g` +
`teardown_appcontext`), não um compartilhado entre requisições
concorrentes — decisão ligada ao refactor do Context Manager (ver
Fase 3). Tratamento de erros mapeia as 3 famílias de
`shared.exceptions` para HTTP, incluindo o caso não óbvio dos 7 erros
de "possui dependentes" (ex: `EscolaPossuiDiretorError`), que herdam
de `InfrastructureError` mas viram 409, não 500, por serem
semanticamente um conflito do cliente. Documentação OpenAPI 3.0.3
escrita à mão em `interface/openapi.yaml` (validada estruturalmente,
não só sintaxe YAML — 40 operações, 26 schemas), servida crua em
`/openapi.yaml` e interativa via Swagger UI em `/docs` (CDN, sem
dependência Python de parsing YAML em runtime). 65 testes de
interface, dos 284 do projeto.

---

# Fase 6 — Segurança

Objetivo: controlar acesso ao sistema.

- [ ] Login
- [ ] Autenticação
- [ ] Autorização
- [ ] Permissões por perfil

---

# Fase 7 — Banco de Produção

- [ ] PostgreSQL
- [ ] Configuração por ambiente
- [ ] Migrações

---

# Fase 8 — Qualidade

## Testes

- [ ] Cobertura acima de 90%

## Ferramentas

- [ ] Ruff
- [ ] Black
- [ ] MyPy
- [ ] Pytest

## Integração Contínua

- [ ] GitHub Actions

---

# Fase 9 — Deploy

- [ ] Docker
- [ ] Docker Compose
- [ ] Variáveis de ambiente
- [ ] Deploy

---

# Melhorias Arquiteturais

Estas melhorias podem ser implementadas conforme a necessidade do projeto.

- [x] Context Manager para transações
- [x] Refatoração dos repositórios
- [ ] Unit of Work
- [ ] BaseRepository
- [ ] Repository Factory
- [ ] Suporte a múltiplos bancos
- [ ] Background Jobs
- [ ] Eventos de domínio

---

# Futuras Funcionalidades

- [ ] Dashboard
- [ ] Pesquisa avançada
- [ ] Paginação
- [ ] Exportação para Excel
- [ ] Importação via interface Web
- [ ] Logs de auditoria

---

# Próximo Objetivo

~~Concluir a camada de infraestrutura.~~
Feito — Context Manager adotado pelos 8 repositórios,
`Container.finalizar()` e `GerenciadorDeTransacaoSqlite` testados
(ver Fase 3 e Melhorias Arquiteturais).

## Infraestrutura

- [x] Implementar Context Manager
- [x] Refatorar todos os repositórios
- [x] Padronizar gerenciamento das transações
- [x] Executar todos os testes (258/258)

~~Documentação OpenAPI — único item que falta pra fechar o checklist
original da Fase 5.~~
~~Decisão em aberto pra depois disso: os 2 itens que sobraram da Fase 4
(leitor Excel, orquestrador único que rode os 8 importadores em
ordem), ou seguir para a Fase 6 (Segurança)?~~
Feito — os dois caminhos foram fechados juntos: Fase 4 (leitor Excel,
orquestrador único) e Fase 5 (OpenAPI) estão ambas ✅ agora. 284/284
testes passando.

## Próxima etapa

Fase 6 — Segurança (Login, Autenticação, Autorização, Permissões por
perfil) é a próxima fase não iniciada na ordem do roadmap. Sem
decisão ainda tomada sobre isso — as Fases 1-5 estão todas fechadas,
então esta é a primeira vez que "seguir a ordem" e "não ter nada mais
adiado" apontam pro mesmo lugar.