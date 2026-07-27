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
| Infraestrutura | 🟡 |
| Importação Inicial | ⬜ |
| API REST | ⬜ |
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

---

# Fase 4 — Importação Inicial

## Leitura

- [ ] Leitor CSV/Excel
- [ ] Normalização dos dados
- [ ] Conversão para DTOs

## Importadores

- [ ] DRE
- [ ] Escola
- [ ] Diretor
- [ ] CEMEP
- [ ] Chromebook
- [ ] Responsável
- [ ] Turma
- [ ] Starlink

## Orquestração

- [ ] Ordem correta de importação
- [ ] Registro de erros
- [ ] Relatório final
- [ ] Reimportação das linhas com erro

---

# Fase 5 — API REST

Objetivo: disponibilizar os casos de uso via HTTP.

## Estrutura

- [ ] Flask
- [ ] Blueprints
- [ ] Configurações
- [ ] Injeção de dependências

## Controllers

- [ ] DRE
- [ ] Escola
- [ ] Diretor
- [ ] CEMEP
- [ ] Chromebook
- [ ] Responsável
- [ ] Turma
- [ ] Starlink

## API

- [ ] CRUD completo
- [ ] Tratamento global de exceções
- [ ] Serialização dos DTOs
- [ ] Documentação OpenAPI

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

- [ ] Context Manager para transações
- [ ] Refatoração dos repositórios
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

Concluir a camada de infraestrutura.

## Infraestrutura

- [ ] Implementar Context Manager
- [ ] Refatorar todos os repositórios
- [ ] Padronizar gerenciamento das transações
- [ ] Executar todos os testes

## Próxima etapa

Iniciar a Importação Inicial utilizando os casos de uso existentes.