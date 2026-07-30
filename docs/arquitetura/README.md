# 🖥 CITBD Frontend

Frontend do sistema **CITBD**, responsável pela interface do usuário e pela comunicação com a API do backend.

O projeto foi desenvolvido utilizando **React**, **TypeScript** e **Vite**, seguindo uma arquitetura **Feature-Based**, com foco em simplicidade, desempenho, desacoplamento e escalabilidade.

---

# 📌 Objetivo

O frontend tem como objetivo oferecer uma interface intuitiva para gerenciamento das informações das escolas da rede estadual do Pará.

A aplicação foi projetada para:

- Ser simples de utilizar;
- Priorizar a experiência do usuário (UX);
- Facilitar a manutenção do código;
- Evoluir sem impactar outros módulos do sistema;
- Consumir exclusivamente a API do backend.

---

# 🎯 Princípios

Durante o desenvolvimento deste projeto são seguidos os seguintes princípios:

- Interface simples e objetiva;
- Componentes reutilizáveis;
- Baixo acoplamento entre módulos;
- Alta coesão;
- Organização por funcionalidades (Feature-Based);
- Separação de responsabilidades;
- Código legível;
- Evolução incremental;
- Performance antes de complexidade.

---

# 🏛 Arquitetura

O frontend é uma **Single Page Application (SPA)** construída em React.

Toda comunicação ocorre exclusivamente através da API do backend.

```text
               Usuário
                   │
                   ▼
          React + TypeScript
                   │
            HTTP / JSON (REST)
                   │
                   ▼
           Backend (FastAPI)
```

O frontend não possui regras de negócio.

Sua responsabilidade é:

- apresentar informações;
- coletar dados do usuário;
- consumir a API;
- gerenciar navegação e estado da interface.

---

# 📁 Estrutura do Projeto

```text
frontend/
│
├── public/
│
├── src/
│   │
│   ├── app/
│   │
│   ├── shared/
│   │
│   ├── features/
│   │
│   ├── assets/
│   │
│   └── main.tsx
│
├── package.json
│
└── vite.config.ts
```

---

# 📦 Organização

## app/

Responsável pela inicialização da aplicação.

Exemplos:

- App
- Router
- Providers

---

## shared/

Contém recursos reutilizáveis por qualquer módulo.

Exemplos:

- Componentes de UI
- Layouts
- Hooks compartilhados
- Serviços comuns
- Tipos
- Utilitários
- Estilos globais

Nenhum arquivo desta pasta deve conter regras específicas de uma funcionalidade.

---

## features/

Cada funcionalidade da aplicação possui seu próprio módulo.

Exemplo:

```text
features/

├── dashboard/
├── escolas/
├── diretores/
├── cemep/
├── chromebooks/
├── starlink/
├── importacao/
└── usuarios/
```

Cada feature é independente das demais.

---

# 📂 Estrutura de uma Feature

```text
escolas/

├── components/
│
├── hooks/
│
├── pages/
│
├── services/
│
├── types/
│
└── routes.ts
```

Tudo relacionado ao módulo Escola permanece dentro dessa estrutura.

---

# 🔄 Fluxo de Dados

A comunicação com a API segue sempre o mesmo fluxo.

```text
Página

↓

Componente

↓

Hook

↓

Service

↓

API REST

↓

Backend
```

As páginas nunca acessam a API diretamente.

---

# 🧩 Componentes Compartilhados

Os componentes reutilizáveis ficam em:

```text
shared/components/
```

Exemplos:

- Button
- Card
- Modal
- Table
- Input
- Badge
- Header
- Sidebar

Esses componentes não conhecem regras de negócio.

---

# 🌐 Comunicação com a API

Toda comunicação com o backend é centralizada na camada de serviços.

Exemplo:

```text
features/escolas/services/
```

Os componentes nunca utilizam chamadas HTTP diretamente.

---

# 🚀 Como executar

Instale as dependências

```bash
npm install
```

Execute o projeto

```bash
npm run dev
```

Build de produção

```bash
npm run build
```

---

# 🔒 Autenticação

A autenticação ainda não faz parte da primeira versão do sistema.

A arquitetura, entretanto, foi preparada para suportar futuramente:

- Login de usuários;
- JWT;
- Rotas protegidas;
- Controle de permissões.

---

# 📚 Tecnologias

- React
- TypeScript
- Vite
- React Router
- Tailwind CSS
- Axios

---

# 📖 Convenções

Durante o desenvolvimento seguimos algumas regras:

- Cada arquivo possui uma única responsabilidade.
- Componentes devem ser pequenos e reutilizáveis.
- Não criar abstrações sem necessidade.
- Não adicionar bibliotecas sem resolver um problema real.
- Preferir composição à duplicação.
- Toda feature deve seguir a mesma estrutura.
- Código deve ser fácil de localizar e compreender.

---

# 📈 Evolução

Novas funcionalidades serão adicionadas mantendo a mesma arquitetura.

O objetivo é permitir que o sistema cresça preservando a organização, a legibilidade e a facilidade de manutenção.