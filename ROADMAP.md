# 🗺️ Roadmap

Sistema para gerenciamento de dados da CIT sobre escolas do Estado do Pará.

Projeto desenvolvido para estudo de **Python**, **Domain-Driven Design (DDD)** e
**Clean Architecture**, evoluindo gradualmente até uma aplicação pronta para
produção.

---

# Status Geral

| Etapa       | Status |
|-------------|--------|
| Domínio        | ✅ | 
| Casos de Uso   | ✅ |
| Infraestrutura | 🟡 |
| API REST       | ⬜ |
| Autenticação   | ⬜ |
| Deploy         | ⬜ |

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

## Casos de uso

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
- [x] Connection
- [x] Schema separado

## Repositórios SQLite

- [ ] DRE
- [ ] Escola
- [ ] Diretor
- [x] CEMEP *(em andamento como referência)*
- [ ] Chromebook
- [ ] Responsável
- [ ] Turma
- [ ] Starlink

## Tratamento de erros

- [ ] Traduzir exceções SQLite
- [ ] Padronizar todos os repositórios
- [ ] Refatorar usando Context Manager

## Testes

- [ ] Testes dos repositórios
- [ ] Testes de integração

---

# Fase 4 — API REST

Objetivo: disponibilizar os casos de uso via HTTP.

## Flask

- [ ] Estrutura inicial
- [ ] Blueprints
- [ ] Configurações

## Controllers

- [ ] DRE
- [ ] Escola
- [ ] Diretor
- [ ] CEMEP
- [ ] Chromebook
- [ ] Responsável
- [ ] Turma
- [ ] Starlink

## Endpoints

- [ ] CRUD completo

---

# Fase 5 — Segurança

Objetivo: controlar acesso ao sistema.

- [ ] Login
- [ ] Autenticação
- [ ] Autorização
- [ ] Permissões por perfil

---

# Fase 6 — Banco de Produção

- [ ] PostgreSQL
- [ ] Configuração por ambiente
- [ ] Migrações

---

# Fase 7 — Qualidade

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

# Fase 8 — Deploy

- [ ] Docker
- [ ] Docker Compose
- [ ] Variáveis de ambiente
- [ ] Deploy

---

# Melhorias Arquiteturais

Essas tarefas não adicionam funcionalidades, mas melhoram a arquitetura.

- [ ] Context Manager para tratamento de erros
- [ ] BaseRepository
- [ ] Unit of Work
- [ ] Repository Factory
- [ ] Configuração para múltiplos bancos de dados

---

# Futuras Funcionalidades

- [ ] Dashboard
- [ ] Pesquisa avançada
- [ ] Paginação
- [ ] Exportação para Excel
- [ ] Importação de planilhas
- [ ] Logs de auditoria

---

# Próximo objetivo

Finalizar a camada de infraestrutura.

- [ ] Implementar todos os repositórios SQLite
- [ ] Padronizar tratamento de exceções
- [ ] Criar testes dos repositórios
- [ ] Refatorar utilizando Context Manager