<<<<<<< HEAD
# 🏫 ProjetoBD CIT

Sistema para gerenciamento das informações da **Coordenação de Inovação e Tecnologia (CIT)** sobre as escolas do Estado do Pará.

O projeto está sendo desenvolvido como estudo de **Python**, **Domain-Driven Design (DDD)**, **Clean Architecture** e boas práticas de engenharia de software, evoluindo gradualmente até uma aplicação pronta para produção.
=======
# 🏫 CITBD

Sistema para gerenciamento das informações da **Coordenação de Inovação e Tecnologia (CIT)** das escolas da rede estadual do Pará.

O objetivo do projeto é centralizar informações sobre escolas, equipamentos, conectividade e projetos, reduzindo a dependência de planilhas e oferecendo uma base organizada para consulta e gerenciamento dos dados.

Além da aplicação em si, o projeto também serve como estudo prático de **Domain-Driven Design (DDD)**, **Clean Architecture** e boas práticas de engenharia de software.

---

# 📌 Status do Projeto

🚧 Em desenvolvimento

Atualmente o projeto está sendo desenvolvido de forma incremental, priorizando uma arquitetura desacoplada e de fácil evolução.
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)

---

# 🎯 Objetivos

<<<<<<< HEAD
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
=======
* Centralizar informações das escolas da rede estadual do Pará.
* Facilitar a gestão dos recursos administrados pela Coordenação de Inovação e Tecnologia.
* Servir como projeto de estudo em Arquitetura de Software.
* Aplicar conceitos modernos de desenvolvimento Full Stack.
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)

---

# 🏛 Arquitetura

<<<<<<< HEAD
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
=======
O sistema é composto por duas aplicações independentes que se comunicam exclusivamente por meio de uma API REST.

```text
                Usuário
                   │
                   ▼
        Frontend (React + TypeScript)
                   │
             HTTP / JSON
                   │
                   ▼
        Backend (FastAPI + Python)
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 Presentation           Application
                               │
                               ▼
                            Domain
                               ▲
                               │
                      Infrastructure
```

Essa separação permite que frontend e backend evoluam de forma independente, mantendo baixo acoplamento e alta coesão.

---

# 📁 Estrutura do Projeto

```text
citbd/
│
├── backend/
├── frontend/
├── docs/
├── .gitignore
└── README.md
```
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)

---

# 🛠 Tecnologias

<<<<<<< HEAD
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
=======
## Backend

* Python
* FastAPI
* SQLite
* Pytest
* Ruff
* MyPy

## Frontend

* React
* TypeScript
* Vite
* React Router
* Tailwind CSS
* Axios
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)

---

# 🚀 Como executar

<<<<<<< HEAD
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
=======
## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux
source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)
```

---

<<<<<<< HEAD
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
=======
# 📚 Documentação

A documentação do projeto está organizada na pasta `docs/`.

Principais documentos:

```text
docs/
├── arquitetura/
├── dominio/
├── api/
├── banco/
├── importacao-csv/
└── roadmap.md
```

Documentações específicas também podem ser encontradas em:

```text
backend/README.md
frontend/README.md
```

---

# 📋 Funcionalidades

Entre as funcionalidades previstas para o sistema estão:

* Cadastro de escolas
* Cadastro de DREs
* Cadastro de diretores
* Gerenciamento de projetos
* Controle de equipamentos
* Gerenciamento de conectividade
* Importação de dados via CSV
* Consulta e atualização de informações

---

# 👨‍💻 Autor

Desenvolvido por **Luiz Paulo** como projeto de estudo em *Engenharia de Software*, com foco em *Domain-Driven Design (DDD)*, *Clean Architecture* e desenvolvimento *Full Stack*.
>>>>>>> 963e2a3 (Reorganiza projeto em backend, frontend e docs)
