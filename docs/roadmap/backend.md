# 🗺️ Roadmap do Backend

Backend do **CITBD**, sistema para gerenciamento das informações da Coordenação de Inovação e Tecnologia (CIT) das escolas da rede estadual do Pará.

O backend é desenvolvido de forma incremental, aplicando conceitos de **Engenharia de Software**, **Domain-Driven Design (DDD)** e **Clean Architecture**.

---

# 📊 Status Geral

| Camada                  | Status |
| ----------------------- | ------ |
| Domain                  | ✅      |
| Application             | ✅      |
| Infrastructure          | 🟡     |
| Presentation (API REST) | ⬜      |
| Qualidade               | ⬜      |
| Documentação            | ⬜      |
| Deploy                  | ⬜      |

---

# ✅ Fase 1 — Domain

**Objetivo:** modelar corretamente as regras de negócio.

## Entidades

* [x] DRE
* [x] Escola
* [x] Diretor
* [x] CEMEP
* [x] Responsável
* [x] Turma CEMEP
* [x] Chromebook
* [x] Starlink

## Value Objects

* [x] Nome
* [x] Email
* [x] Telefone
* [x] Município
* [x] Endereço
* [x] Quantidade
* [x] Comentário

## Outros

* [x] Repositórios (interfaces)
* [x] IDs tipados
* [x] Enums
* [x] Exceções de domínio

---

# ✅ Fase 2 — Application

**Objetivo:** implementar os casos de uso.

## Casos de Uso

* [x] CRUD de DRE
* [x] CRUD de Escola
* [x] CRUD de Diretor
* [x] CRUD de CEMEP
* [x] CRUD de Chromebook
* [x] CRUD de Responsável
* [x] CRUD de Turma
* [x] CRUD de Starlink

## DTOs

* [x] Input DTOs
* [x] Output DTOs

## Exceções

* [x] Registro não encontrado
* [x] Registro duplicado
* [x] Relação inexistente

---

# Fase 3 — Infraestrutura 🟡

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
mensagens do SQLite, que vêm em inglês) foram corrigidos. Os 191
testes do projeto passam hoje. O 🟡 permanece porque o Context
Manager (`transacao.py`) segue implementado mas sem uso por nenhum
repositório.

---

# Fase 4 — Importação Inicial 🟡

## Leitura

- [x] Leitor CSV
- [ ] Leitor Excel
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

- [ ] Ordem correta de importação (a ordem DRE → Escola → CEMEP → Responsável → Turma, com Diretor/Chromebook/Starlink dependendo só de Escola, está documentada em cada script e coberta por teste de cadeia completa — falta um comando único que rode os 8 nessa ordem sozinho)
- [x] Registro de erros
- [x] Relatório final
- [x] Reimportação das linhas com erro

Implementado como um `ImportadorPipeline` genérico (Strategy +
Protocol, streaming via `yield`) reutilizado pelas 8 entidades — ver
`docs/importacao.md` para a arquitetura completa. 191 testes
automatizados cobrem o projeto, 49 deles este módulo.

---

# ⬜ Fase 5 — API REST

**Objetivo:** disponibilizar os casos de uso via HTTP.

## Estrutura

* [ ] FastAPI
* [ ] Rotas
* [ ] Configurações
* [ ] Injeção de dependências

## Endpoints

* [ ] DRE
* [ ] Escola
* [ ] Diretor
* [ ] CEMEP
* [ ] Chromebook
* [ ] Responsável
* [ ] Turma
* [ ] Starlink

## API

* [ ] CRUD completo
* [ ] Tratamento global de exceções
* [ ] Serialização dos DTOs
* [ ] Documentação OpenAPI

---

# ⬜ Fase 6 — Segurança

**Objetivo:** controlar o acesso ao sistema.

* [ ] Login
* [ ] Autenticação
* [ ] Autorização
* [ ] Controle de permissões

---

# ⬜ Fase 7 — Qualidade

## Testes

* [ ] Cobertura superior a 90%
* [ ] Testes end-to-end

## Ferramentas

* [ ] Ruff
* [ ] Black
* [ ] MyPy
* [ ] Pytest

## Integração Contínua

* [ ] GitHub Actions

---

# ⬜ Fase 8 — Documentação

## Backend

* [ ] README do backend

## Arquitetura

* [ ] Documentação da arquitetura
* [ ] Diagramas da arquitetura

## Domain

* [ ] Documentação das entidades
* [ ] Documentação dos Value Objects
* [ ] Documentação das regras de negócio

## Application

* [ ] Documentação dos casos de uso

## Infrastructure

* [ ] Documentação da persistência

## API

* [ ] Documentação dos endpoints
* [ ] Exemplos de requisições e respostas

---

# ⬜ Fase 9 — Deploy

* [ ] Docker
* [ ] Docker Compose
* [ ] Variáveis de ambiente
* [ ] Deploy

---

# 💡 Evoluções Arquiteturais

Estas melhorias poderão ser implementadas conforme a evolução do projeto.

* [ ] Context Manager para transações
* [ ] Unit of Work
* [ ] BaseRepository
* [ ] Repository Factory
* [ ] Suporte a múltiplos bancos de dados
* [ ] Background Jobs
* [ ] Eventos de domínio

---

# Futuras Funcionalidades

* [ ] Dashboard
* [ ] Pesquisa avançada
* [ ] Paginação
* [ ] Exportação para Excel
* [ ] Importação via interface Web
* [ ] Logs de auditoria

---

# Próximo Objetivo

Concluir a camada de infraestrutura.

## Infraestrutura

- [ ] Implementar Context Manager (arquivo existe em `transacao.py`, mas nenhum repositório o usa ainda)
- [ ] Refatorar todos os repositórios
- [ ] Padronizar gerenciamento das transações
- [x] Executar todos os testes (191/191 — ver nota na Fase 3)

## Próxima etapa

~~Iniciar a Importação Inicial utilizando os casos de uso existentes.~~
Feito — os 8 importadores estão implementados e testados (Fase 4).
