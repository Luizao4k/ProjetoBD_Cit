# 🏫 CITBD Backend

Backend do sistema **CITBD**, responsável pelo gerenciamento das informações da Coordenação de Inovação e Tecnologia (CIT) sobre as escolas da rede estadual do Pará.

Este projeto está sendo desenvolvido como estudo de arquitetura de software, utilizando **Python**, **Domain-Driven Design (DDD)** e **Clean Architecture**, com foco em código desacoplado, legível, testável e escalável.

---

# 📌 Sobre o projeto

O backend é responsável por centralizar as regras de negócio do sistema, disponibilizando casos de uso para gerenciamento das informações das escolas e seus recursos tecnológicos.

Toda a modelagem foi construída priorizando:

- Independência de frameworks
- Baixo acoplamento
- Alta coesão
- Testabilidade
- Evolução incremental

---

# 🎯 Objetivos

Além de atender às necessidades do sistema, este projeto tem como objetivo consolidar conhecimentos em:

- Python
- Domain-Driven Design (DDD)
- Clean Architecture
- SOLID
- Arquitetura em camadas
- APIs REST
- Testes automatizados
- Injeção de Dependências
- Persistência de dados
- Refatoração e boas práticas

---

# 📚 Domínio

O sistema gerencia informações relacionadas às escolas da rede pública estadual do Pará.

## Principais módulos

- DRE
- Escola
- Diretor
- CEMEP
- Responsável
- Turma CEMEP
- Chromebook
- Starlink

As regras de negócio permanecem isoladas na camada de domínio, sem dependência de banco de dados, frameworks ou bibliotecas externas.

---

# 🏛 Arquitetura

O projeto segue os princípios da **Clean Architecture**, organizando o código em camadas independentes.

```
backend/

├── application/
│
├── domain/
│
├── infrastructure/
│
├── presentation/
│
├── tests/
│
└── shared/
```

## Camadas

### Domain

Núcleo da aplicação.

Contém as entidades, Value Objects, regras de negócio, interfaces de repositórios e exceções de domínio.

Não depende de nenhuma tecnologia externa.

---

### Application

Implementa os casos de uso do sistema.

Cada funcionalidade representa uma ação executada pelo usuário e orquestra a comunicação entre domínio e infraestrutura.

---

### Infrastructure

Responsável pela comunicação com tecnologias externas.

Exemplos:

- Banco de dados
- Repositórios
- Importação de arquivos
- Containers de dependência
- Persistência

---

### Presentation

Responsável pela exposição da aplicação.

Nesta camada ficam os controladores, rotas, validações de entrada e integração com a API.

---

# 🛠 Tecnologias

- Python
- SQLite
- Pytest
- Ruff
- MyPy

---

# 📁 Estrutura do projeto

```
backend/

├── application/
├── domain/
├── infrastructure/
├── presentation/
├── script/
├── shared/
└── tests/
```

---

# 🚀 Como executar

Clone o projeto

```bash
git clone <repositorio>
```

Entre na pasta

```bash
cd backend
```

Crie o ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente

### Windows

```bash
.venv\Scripts\activate
```

### Linux

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

# 🧪 Testes

O projeto possui testes automatizados para garantir a estabilidade das regras de negócio e dos casos de uso.

À medida que novas funcionalidades forem implementadas, novos testes serão adicionados seguindo a mesma filosofia de desenvolvimento orientado à qualidade.

---

# 📚 Documentação

A documentação da arquitetura e das decisões técnicas encontra-se na pasta **docs/** do projeto principal.

---

# 🛣 Roadmap

A evolução do projeto pode ser acompanhada através do arquivo:

```
ROADMAP.md
```

---

# 👨‍💻 Autor

Desenvolvido por **Luiz Paulo** como projeto de estudo e aprimoramento em arquitetura de software, Domain-Driven Design e Clean Architecture.