# 🏫 ProjetoBD CIT

Sistema para gerenciamento das informações da **Coordenação de Inovação e Tecnologia (CIT)** sobre as escolas do Estado do Pará.

O projeto está sendo desenvolvido como estudo de **Python**, **Domain-Driven Design (DDD)**, **Clean Architecture** e boas práticas de engenharia de software, evoluindo gradualmente até uma aplicação pronta para produção.

---

# 🎯 Objetivos

Este projeto tem como foco o aprendizado de:

- Python
- Domain-Driven Design (DDD)
- Clean Architecture
- SOLID
- Testes automatizados
- Arquitetura em camadas
- Repositórios
- DTOs
- Banco de Dados
- APIs REST
- Injeção de Dependências

---

# 📚 Domínio

O sistema gerencia informações relacionadas às escolas da rede pública do Estado do Pará.

## Principais entidades

- DRE (Diretoria Regional de Ensino)
- Escola
- Diretor
- CEMEP
- Responsável
- Turma CEMEP
- Chromebook
- Starlink

As regras de negócio são modeladas utilizando princípios de DDD, mantendo a camada de domínio totalmente independente das demais.

---

# 🏛 Arquitetura

O projeto segue a arquitetura em camadas inspirada na Clean Architecture.

```
.
├── application/
│   └── use_cases/
│
├── domain/
│   ├── entities/
│   ├── repositories/
│   ├── value_objects/
│   ├── enums/
│   ├── exceptions/
│   └── factories/
│
├── infrastructure/
│   ├── database/
│   ├── repositories/
│   ├── container/
│   └── schemas/
│
├── shared/
│
├── tests/
│
└── ROADMAP.md
```

### Camadas

### Domain

Contém:

- Entidades
- Value Objects
- Regras de negócio
- Interfaces de Repositórios
- Exceções de domínio

Não possui dependência de banco de dados, frameworks ou bibliotecas externas.

---

### Application

Responsável pelos casos de uso da aplicação.

Cada funcionalidade é implementada como um **Use Case**, utilizando DTOs de entrada e saída.

Exemplos:

- Criar Escola
- Atualizar Escola
- Buscar Escola
- Remover Escola

---

### Infrastructure

Responsável pela comunicação com tecnologias externas.

Exemplos:

- SQLite
- Repositórios
- Connection Factory
- Container de dependências

---

# 🛠 Tecnologias

- Python 3.14+
- SQLite
- Pytest
- Ruff
- MyPy
- Clean Architecture
- Domain-Driven Design

---

# ✅ Funcionalidades implementadas

## Domínio

- Entidades
- Value Objects
- Repositórios (interfaces)
- Enums
- Exceções
- IDs tipados

## Aplicação

CRUD completo para:

- DRE
- Escola
- Diretor
- CEMEP
- Chromebook
- Responsável
- Turma CEMEP
- Starlink

Todos os casos de uso utilizam DTOs para entrada e saída.

## Infraestrutura

- SQLite
- Connection Factory
- Repositórios SQLite
- Container de dependências
- Testes de integração

---

# 🚀 Como executar

Clone o projeto

```bash
git clone https://github.com/seu-usuario/ProjetoBD_Cit.git
```

Entre na pasta

```bash
cd ProjetoBD_Cit
```

Crie o ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Execute os testes

```bash
pytest
```

---

# 📈 Roadmap

O progresso do desenvolvimento pode ser acompanhado em:

**ROADMAP.md**

---

# 📖 Aprendizados

Este projeto é utilizado como laboratório para praticar conceitos como:

- Arquitetura limpa
- DDD
- Testes automatizados
- Refatoração
- Boas práticas de modelagem
- Organização de projetos Python

---

# 📄 Licença

Projeto desenvolvido por Luiz Paulo para fins de estudo.
