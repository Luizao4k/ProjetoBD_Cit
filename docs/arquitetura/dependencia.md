# 🔗 Dependências entre as Camadas

A arquitetura do **CITBD** segue o princípio da **Inversão de Dependências (Dependency Inversion Principle)**, um dos pilares da **Clean Architecture**.

O objetivo é garantir que as regras de negócio permaneçam independentes de frameworks, banco de dados e detalhes de implementação.

---

# Regra Fundamental

As dependências sempre apontam para o centro da aplicação.

```text
Presentation
      │
      ▼
Application
      │
      ▼
Domain
      ▲
      │
Infrastructure
```

O **Domain** é a camada mais importante do sistema.

Nenhuma decisão técnica deve influenciar sua implementação.

---

# Relação entre as Camadas

## Presentation → Application

A camada de apresentação depende da camada de aplicação.

Ela não possui regras de negócio.

Sua responsabilidade é apenas:

- Receber requisições
- Validar dados básicos
- Executar casos de uso
- Construir respostas HTTP

Ela nunca manipula diretamente entidades do domínio.

---

## Application → Domain

A camada de aplicação depende exclusivamente do domínio.

Ela coordena a execução dos casos de uso utilizando:

- Entidades
- Value Objects
- Serviços de Domínio
- Interfaces de Repositórios

Ela não conhece banco de dados nem frameworks.

---

## Infrastructure → Domain

A infraestrutura implementa as interfaces definidas pelo domínio.

Exemplo:

```python
class EscolaRepository(Protocol):
    ...
```

O domínio define **o contrato**.

A infraestrutura fornece **a implementação**.

Por exemplo:

```text
Domain
└── EscolaRepository

Infrastructure
└── SqliteEscolaRepository
```

Dessa forma, é possível trocar SQLite por PostgreSQL sem alterar o domínio.

---

# Dependências Permitidas

| Camada | Pode depender de |
|---------|------------------|
| Presentation | Application |
| Application | Domain |
| Domain | Nenhuma camada do projeto |
| Infrastructure | Domain |

---

# Dependências Proibidas

Estas dependências violam a arquitetura do projeto.

❌ Domain → Infrastructure

```text
Domain
    │
    ▼
SQLite
```

O domínio nunca deve conhecer detalhes do banco.

---

❌ Domain → FastAPI

```text
Domain
    │
    ▼
FastAPI
```

Frameworks pertencem à infraestrutura ou apresentação.

---

❌ Application → SQLite

Os casos de uso nunca acessam diretamente o banco de dados.

Toda persistência ocorre por meio das interfaces de repositório.

---

❌ Presentation → Banco de Dados

Controllers não realizam consultas diretamente.

Toda operação deve passar pelos casos de uso.

---

# Exemplo de Fluxo

```text
HTTP Request
      │
      ▼
Controller
      │
      ▼
Caso de Uso
      │
      ▼
Repository Interface
      │
      ▼
Repository SQLite
      │
      ▼
Banco de Dados
```

Observe que o Caso de Uso conhece apenas a interface do repositório.

A implementação concreta é responsabilidade da infraestrutura.

---

# Benefícios

Seguir essa direção de dependências traz diversas vantagens:

- Independência de frameworks
- Facilidade para trocar banco de dados
- Maior testabilidade
- Baixo acoplamento
- Alta coesão
- Reutilização do domínio
- Facilidade de manutenção
- Evolução incremental da aplicação

---

# Princípios Aplicados

Esta organização utiliza principalmente:

- SOLID
  - Dependency Inversion Principle (DIP)
  - Single Responsibility Principle (SRP)

- Clean Architecture
  - Independência de frameworks
  - Independência do banco de dados
  - Independência da interface do usuário

- Domain-Driven Design (DDD)
  - Modelo de domínio rico
  - Interfaces de repositórios
  - Regras de negócio centralizadas no domínio