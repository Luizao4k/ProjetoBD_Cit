# 🏛 Arquitetura Geral

O **CITBD** é composto por duas aplicações independentes: **Frontend** e **Backend**. A comunicação entre elas ocorre exclusivamente por meio de uma **API REST**, permitindo que ambas evoluam de forma desacoplada.

O backend segue os princípios da **Clean Architecture** e do **Domain-Driven Design (DDD)**, mantendo as regras de negócio independentes de frameworks, banco de dados e demais detalhes de implementação.

---

# Visão Geral

```text
                            Usuário
                                │
                                ▼
                 Frontend (React • TypeScript • Vite)
                                │
                         HTTP / JSON (REST)
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │            Presentation Layer                 │
        │      FastAPI • Controllers • DTOs             │
        └───────────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │            Application Layer                  │
        │      Use Cases • DTOs • Orquestração          │
        └───────────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │               Domain Layer                    │
        │ Entities • Value Objects • Enums             │
        │ Repository Interfaces • Domain Services      │
        └───────────────────────────────────────────────┘
                   ▲                           ▲
                   │                           │
        ┌────────────────────┐     ┌────────────────────┐
        │ Infrastructure      │     │ Serviços Externos │
        │ SQLite              │     │ CSV               │
        │ Repository Impl.    │     │ APIs Futuras      │
        │ Dependency Injection│     │                   │
        └────────────────────┘     └────────────────────┘
                   │
                   ▼
             Banco de Dados
```

---

# Organização da Arquitetura

O sistema está dividido em duas aplicações independentes.

## Frontend

Responsável pela interação com o usuário.

Suas responsabilidades incluem:

- Interface gráfica
- Navegação
- Validação básica dos formulários
- Consumo da API REST
- Exibição das informações

---

## Backend

Responsável por toda a lógica de negócio da aplicação.

Está organizado em quatro camadas principais:

```text
Presentation
      │
Application
      │
Domain
      ▲
      │
Infrastructure
```

As dependências sempre apontam para o centro da arquitetura, garantindo que o domínio permaneça independente de tecnologias externas.

---

# Responsabilidades das Camadas

## Presentation

É a porta de entrada do backend.

Responsabilidades:

- Receber requisições HTTP
- Validar dados de entrada
- Chamar os casos de uso
- Converter respostas para HTTP

---

## Application

Coordena o funcionamento da aplicação.

Responsabilidades:

- Implementar os casos de uso
- Orquestrar o domínio
- Coordenar operações entre entidades e repositórios
- Retornar DTOs

Esta camada não implementa regras de negócio complexas; ela apenas coordena sua execução.

---

## Domain

Representa o núcleo da aplicação.

É composto por:

- Entidades
- Value Objects
- Enums
- Interfaces de Repositório
- Serviços de Domínio
- Regras de negócio

O domínio não depende de frameworks, banco de dados ou bibliotecas externas.

---

## Infrastructure

Implementa os detalhes técnicos necessários para executar a aplicação.

Responsabilidades:

- Persistência dos dados
- Implementação dos repositórios
- Configuração do banco de dados
- Importação de arquivos
- Integração com serviços externos
- Injeção de dependências

Toda dependência tecnológica permanece concentrada nesta camada.

---

# Fluxo de uma Requisição

Uma requisição percorre o sistema seguindo o fluxo abaixo:

```text
Usuário
    │
    ▼
Frontend
    │
    ▼
Controller
    │
    ▼
Caso de Uso
    │
    ▼
Entidades / Repositórios
    │
    ▼
Infrastructure
    │
    ▼
Banco de Dados
```

Após a execução, a resposta retorna pelo mesmo caminho até o usuário.

---

# Princípios Arquiteturais

Durante o desenvolvimento do CITBD são adotados os seguintes princípios:

## Clean Architecture

- Separação de responsabilidades
- Independência de frameworks
- Independência do banco de dados
- Independência da interface do usuário
- Inversão de dependências

---

## Domain-Driven Design (DDD)

- Modelo de domínio rico
- Regras de negócio centralizadas
- Value Objects
- Entidades
- Repositórios
- Linguagem ubíqua

---

## SOLID

- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)

---

# Objetivos da Arquitetura

A arquitetura foi projetada para proporcionar:

- Baixo acoplamento
- Alta coesão
- Facilidade de manutenção
- Facilidade de testes
- Evolução incremental
- Reutilização do domínio
- Escalabilidade
- Clareza na organização do código

---

# Documentação Relacionada

Para aprofundar cada aspecto da arquitetura, consulte os documentos específicos:

```text
docs/
└── arquitetura/
    ├── geral.md
    ├── camadas.md
    ├── fluxo-requisicao.md
    └── decisoes.md
```