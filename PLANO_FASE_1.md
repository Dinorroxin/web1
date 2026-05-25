# 📋 Plano Completo: Plataforma Web de Contabilidade — Fase 1 (MVP)

**Data:** 23 de Maio de 2026  
**Status:** Em Planejamento  
**Versão:** 1.1

---

## 🎯 Visão Geral Executiva

### TL;DR
Desenvolver uma **plataforma web responsiva para gestão de contabilidade** com autenticação segura via OAuth2, dashboard interativo para gerenciar empresas (estilo Trello), **leitura de arquivos Excel (.xlsx)** para importação de dados, **geração de PDFs detalhados** com relatórios, e infraestrutura escalável para futuras expansões. 

**MVP (Fase 1)** foca exclusivamente em:
- ✅ Autenticação e Login
- ✅ Layout responsivo com Header e Sidebar
- ✅ Dashboard com CRUD de Empresas
- ✅ Importação de dados via Excel (.xlsx)
- ✅ Geração básica de PDF (estrutura pronta para expansão)

Stack confirmado:
- **Frontend:** React 18 + TypeScript + Vite
- **Backend:** Python FastAPI + Pydantic v2
- **Database:** MongoDB
- **Auth:** OAuth2 (Google/Microsoft) + JWT
- **Excel:** openpyxl (Python) + xlsx (JavaScript)
- **PDF:** ReportLab (Python) ou PDFkit (Python wrapper wkhtmltopdf)
- **Deploy:** Vercel (frontend), Backend a decidir após escalonamento

---

## 🏗️ Arquitetura de Alto Nível

```
┌──────────────────────────────────────────────────────────────┐
│                     CLIENTE (Browser)                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │        Frontend (React 18 + TypeScript)             │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  Auth Pages  │  │  Dashboard   │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  Layout      │  │  Import Excel│               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  PDF Report  │  │  Common Cmps │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  │                                                     │    │
│  │  ├─ Context API (Auth, Company, UI State)         │    │
│  │  ├─ Custom Hooks (useAuth, useCompany, etc)       │    │
│  │  ├─ Axios Service (API calls)                      │    │
│  │  ├─ XLSX library (file upload + parsing)          │    │
│  │  └─ Tailwind CSS + CSS Modules                    │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
                           │
                    HTTPS / REST API
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              SERVIDOR (FastAPI + Python)                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            FastAPI Application                      │   │
│  │                                                      │   │
│  │  ┌────────────────┐  ┌────────────────┐            │   │
│  │  │  /auth         │  │  /companies    │            │   │
│  │  │  - login       │  │  - GET (list)  │            │   │
│  │  │  - oauth2      │  │  - POST (add)  │            │   │
│  │  │  - logout      │  │  - PUT (edit)  │            │   │
│  │  │  - refresh     │  │  - DELETE      │            │   │
│  │  └────────────────┘  └────────────────┘            │   │
│  │  ┌────────────────┐  ┌────────────────┐            │   │
│  │  │  /import       │  │  /reports      │            │   │
│  │  │  - POST upload │  │  - GET pdf/:id │            │   │
│  │  │  - GET status  │  │  - POST create │            │   │
│  │  └────────────────┘  └────────────────┘            │   │
│  │  ┌────────────────┐  ┌────────────────┐            │   │
│  │  │  /notes        │  │  /tags         │            │   │
│  │  │  - GET/POST    │  │  - GET/POST    │            │   │
│  │  │  - PUT/DELETE  │  │  - PUT/DELETE  │            │   │
│  │  └────────────────┘  └────────────────┘            │   │
│  │                                                      │   │
│  │  ├─ Dependencies (JWT validation, DB session)       │   │
│  │  ├─ Services (business logic, Excel parsing)        │   │
│  │  ├─ Models & Schemas (Pydantic)                     │   │
│  │  ├─ Middleware (CORS, error handling)               │   │
│  │  ├─ Excel Service (openpyxl, validação)             │   │
│  │  ├─ PDF Service (geração de relatórios)             │   │
│  │  └─ OAuth2 Service (Google/Microsoft)               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                      Motor (async)
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    MongoDB Atlas                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Collections:                                               │
│  ├─ users        (email, nome, google_id, oauth_provider)  │
│  ├─ companies    (user_id, nome, email, telefone)          │
│  ├─ notes        (company_id, texto, created_at)           │
│  ├─ tags         (user_id, titulo, cor)                    │
│  ├─ company_tags (company_id, tag_id)                      │
│  ├─ imports      (user_id, arquivo, status, dados)         │
│  └─ reports      (user_id, tipo, url_pdf, created_at)      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos Funcionais - MVP

### 1. **Autenticação & Sessão**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-01 | Login com OAuth2 | Usuário pode fazer login via Google ou Microsoft |
| RF-02 | JWT Token | Backend emite JWT com expiração de 1 hora + refresh token |
| RF-03 | Proteção de Rotas | Rotas protegidas redirecionam para login se não autenticado |
| RF-04 | Logout | Usuário pode fazer logout, limpando tokens locais |
| RF-05 | Refresh Token | Frontend solicita novo token automaticamente usando refresh token |
| RF-06 | Persistência de Sessão | Sessão persiste ao recarregar página (se token válido) |

### 2. **Layout & Navegação**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-07 | Header | Contém logo/nome projeto (esquerda), menu do usuário (direita) com dropdown |
| RF-08 | Dropdown Menu | Opções: "Atualizar dados", "Sair", "Configurações" |
| RF-09 | Sidebar Retrátil | Menu com "Dashboard", "Enviar email", "Calendário", "Importar Excel", "Configurações" |
| RF-10 | Hover na Nav | Hovering em item de nav escurece o fundo |
| RF-11 | Seleção Visual | Item selecionado tem linha azul petróleo à esquerda + cor transparente |
| RF-12 | Navegação SPA | Clique em nav muda conteúdo SEM reload de página |
| RF-13 | Responsive Sidebar | Mobile: colapsada por padrão; Desktop: expandida |
| RF-14 | Animações Suaves | Transições de cor, retraimento de sidebar, hover (300ms) |

### 3. **Dashboard (Gerenciamento de Empresas)**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-15 | Listar Empresas | Exibir todas as empresas do usuário em cards estilo Trello |
| RF-16 | Adicionar Empresa | Modal com campos: nome, email, telefone (todos obrigatórios) |
| RF-17 | Validação de Dados | Email deve ser válido (regex), telefone (11 dígitos) |
| RF-18 | Editar Empresa | (Futuro) Clicar no card permite editar |
| RF-19 | Deletar Empresa | (Futuro) Opção de remover empresa com confirmação |
| RF-20 | Adicionar Notas | Botão/form inline para adicionar nota à empresa |
| RF-21 | Preview de Notas | Card mostra resumo da nota mais recente |
| RF-22 | Expandir Empresa | Clicar no card abre detail view com todas as notas |
| RF-23 | Hover no Card | Card escurece levemente ao hovering |
| RF-24 | Sem Reload | Adicionar/editar empresa não recarrega página |

### 4. **Importação de Excel (.xlsx)**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-25 | Upload de Arquivo | Usuário pode fazer upload de arquivo .xlsx no max 10MB |
| RF-26 | Validação de Extensão | Sistema rejeita arquivos que não sejam .xlsx |
| RF-27 | Bloqueio de Macros | Sistema rejeita arquivos .xlsx com macros ativas |
| RF-28 | Leitura de Dados | Parser lê coluna A (nome), B (email), C (telefone) |
| RF-29 | Validação de Dados | Cada linha é validada (email format, phone length) |
| RF-30 | Pré-visualização | Usuário vê preview antes de confirmar importação |
| RF-31 | Importação em Lote | Adiciona todas as empresas válidas ao BD em uma transação |
| RF-32 | Relatório de Importação | Mostra quantas empresas importadas, quantas falharam e porquê |
| RF-33 | Tratamento de Duplicatas | Se empresa já existe (email), pula ou oferece opção de atualizar |
| RF-34 | Histórico de Importação | Lista de imports com data, arquivo, status, total importado |

### 5. **Geração de PDF**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-35 | Gerar PDF | Usuário pode gerar relatório em PDF com dados de empresas |
| RF-36 | Estrutura de PDF | Header (logo, data), tabela de empresas, rodapé (usuário, data) |
| RF-37 | Filtro por Data | PDF pode incluir apenas empresas adicionadas num período |
| RF-38 | Inclusão de Notas | PDF pode incluir resumo de notas por empresa (opcional) |
| RF-39 | Assinatura do Usuário | PDF inclui nome e email do usuário que gerou |
| RF-40 | Download Automático | PDF é baixado automaticamente ou disponível em link |
| RF-41 | Histórico de PDFs | (Futuro) Listar PDFs gerados anteriormente |
| RF-42 | Customização | (Futuro) Usuário define quais colunas incluir no PDF |

### 6. **Notas & Tags (Preparação para Futuro)**

| ID | Requisito | Descrição |
|------|-----------|-----------|
| RF-43 | Adicionar Nota | Usuário pode escrever nota em texto livre (max 500 chars) |
| RF-44 | Listar Notas | Todas as notas da empresa aparecem em cronologia reversa |
| RF-45 | Deletar Nota | (Futuro) Botão para remover nota |
| RF-46 | Tags Customizáveis | (Futuro) Usuário define cores e títulos para tags |
| RF-47 | Associar Tags | (Futuro) Tags podem ser atribuídas a empresas |
| RF-48 | Filtragem por Tag | (Futuro) Dashboard filtra empresas por tag selecionada |

### 7. **Responsividade**

| Breakpoint | Comportamento |
|------------|---------------|
| **xs** (320px) | Sidebar colapsada, botões stack verticalmente |
| **sm** (640px) | Sidebar colapsada, layout mobile otimizado |
| **md** (768px) | Sidebar começa a expandir, layout muda |
| **lg** (1024px) | Sidebar expandida, layout desktop |
| **xl** (1280px+) | Layout otimizado para telas grandes |

---

## 🗂️ Estrutura de Projeto

```
d:\proj_contabilidade/
│
├── docs/                                     # Documentação
│   ├── PLANO_FASE_1.md                      # Este arquivo
│   ├── ARQUITETURA.md                       # (Futuro) Detalhes técnicos
│   ├── API_DOCS.md                          # (Futuro) Especificação endpoints
│   ├── DATABASE.md                          # (Futuro) Schema MongoDB
│   └── SETUP.md                             # (Futuro) Guia instalação
│
├── frontend/                                 # React App
│   ├── public/
│   │   ├── favicon.ico
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   │
│   │   │   ├── Layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── DashboardView.tsx
│   │   │   │   ├── CompanyCard.tsx
│   │   │   │   ├── CompanyGrid.tsx
│   │   │   │   ├── AddCompanyModal.tsx
│   │   │   │   ├── CompanyDetail.tsx
│   │   │   │   └── NotesList.tsx
│   │   │   │
│   │   │   ├── Import/
│   │   │   │   ├── ImportExcelPage.tsx
│   │   │   │   ├── FileUploadZone.tsx
│   │   │   │   ├── PreviewTable.tsx
│   │   │   │   ├── ImportProgress.tsx
│   │   │   │   └── ImportHistory.tsx
│   │   │   │
│   │   │   ├── Reports/
│   │   │   │   ├── ReportsPage.tsx
│   │   │   │   ├── ReportBuilder.tsx
│   │   │   │   ├── ReportPreview.tsx
│   │   │   │   └── ReportHistory.tsx
│   │   │   │
│   │   │   ├── Common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Dropdown.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   └── Toast.tsx
│   │   │   │
│   │   │   └── Pages/
│   │   │       ├── EmailPage.tsx
│   │   │       ├── CalendarPage.tsx
│   │   │       └── ConfigPage.tsx
│   │   │
│   │   ├── context/
│   │   │   ├── AuthContext.tsx
│   │   │   ├── CompanyContext.tsx
│   │   │   ├── ImportContext.tsx
│   │   │   └── UIContext.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useCompany.ts
│   │   │   ├── useImport.ts
│   │   │   ├── useFetch.ts
│   │   │   └── useLocalStorage.ts
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── authService.ts
│   │   │   ├── companyService.ts
│   │   │   ├── importService.ts
│   │   │   ├── reportService.ts
│   │   │   └── noteService.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── excelParser.ts
│   │   │   ├── validators.ts
│   │   │   ├── formatters.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├── variables.css
│   │   │   └── components/
│   │   │
│   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   ├── App.tsx
│   │   └── index.tsx
│   │
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
├── backend/                                  # FastAPI App
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── companies.py
│   │   │   ├── notes.py
│   │   │   ├── tags.py
│   │   │   ├── imports.py
│   │   │   ├── reports.py
│   │   │   ├── users.py
│   │   │   └── router.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── note.py
│   │   │   ├── tag.py
│   │   │   ├── import.py
│   │   │   └── report.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── note.py
│   │   │   ├── auth.py
│   │   │   ├── import.py
│   │   │   └── report.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── company_service.py
│   │   │   ├── oauth_service.py
│   │   │   ├── excel_service.py
│   │   │   ├── pdf_service.py
│   │   │   └── email_service.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── migrations.py
│   │   │
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── cors.py
│   │   │   └── error_handler.py
│   │   │
│   │   ├── dependencies.py
│   │   └── security.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_companies.py
│   │   ├── test_imports.py
│   │   ├── test_reports.py
│   │   └── test_notes.py
│   │
│   ├── uploads/
│   ├── outputs/
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       ├── frontend-ci.yml
│       └── backend-ci.yml
│
├── .gitignore
├── README.md
└── CONTRIBUINDO.md
```

---

## 🎨 Design System & Paleta de Cores

| Nome | Hex | RGB | Uso |
|------|-----|-----|-----|
| **Azul Petróleo** | `#003D5C` | 0, 61, 92 | Header, sidebar selecionado, botões |
| **Branco** | `#FFFFFF` | 255, 255, 255 | Background, texto principal |
| **Cinza Médio** | `#6B7280` | 107, 114, 128 | Texto secundário, borders |
| **Cinza Claro** | `#F3F4F6` | 243, 244, 246 | Hover background |
| **Verde Sucesso** | `#10B981` | 16, 185, 129 | Sucesso, validação |
| **Vermelho Alerta** | `#EF4444` | 239, 68, 68 | Erro, alerta |

---

## 📦 Stack Tecnológico

### Frontend
```json
{
  "react": "^18.2.0",
  "typescript": "^5.0.0",
  "vite": "^5.0.0",
  "axios": "^1.6.0",
  "react-router-dom": "^6.15.0",
  "xlsx": "^0.18.5"
}
```

### Backend
```
FastAPI==0.104.0
uvicorn==0.24.0
pydantic==2.5.0
motor==3.3.2
openpyxl==3.11.0
reportlab==4.0.7
python-jose==3.3.0
python-multipart==0.0.6
```

---

## 🚀 Roadmap Sprint 1 (Setup & Infraestrutura)

- [ ] Inicializar React com Vite
- [ ] Inicializar FastAPI
- [ ] Configurar MongoDB Atlas
- [ ] Setup OAuth2 Google credentials
- [ ] Criar .env files (frontend + backend)
- [ ] Estruturar pastas conforme projeto
- [ ] Setup git e README
- [ ] Testar ambos servidores localmente

---

**Status:** ✅ Pronto para Implementação

