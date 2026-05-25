# 🧠 Chatbot Inteligente para Clínica de Psicologia

Sistema web inteligente para atendimento automatizado, captação de leads e automação de processos clínicos utilizando Inteligência Artificial, Flask, n8n e integrações HTTP.

---

# 📌 Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de criar uma solução moderna para clínicas de psicologia, permitindo:

- Atendimento automatizado via chatbot
- Captação inteligente de leads
- Integração com IA generativa
- Dashboard administrativo
- Exportação de dados
- Automação com n8n
- Integração com Gmail SMTP
- Organização e análise de leads

---

# 🚀 Tecnologias Utilizadas

## Backend
- Python
- Flask
- Flask-Login
- Pandas
- CSV
- Requests
- Threading
- dotenv

## Inteligência Artificial
- Groq API
- OpenAI SDK
- Llama 3.3 70B Versatile

## Automação
- n8n
- Webhooks HTTP

## Comunicação
- Gmail SMTP

## Frontend
- HTML5
- CSS3
- Jinja2

---

# 🧩 Arquitetura da Solução

```text
Usuário
   ↓
Frontend HTML
   ↓
Flask Backend
   ↓
IA Groq/OpenAI
   ↓
Detecção de Lead
   ↓
CSV + Dashboard
   ↓
Webhook HTTP
   ↓
n8n
   ↓
Automações
   ↓
Email / CRM / WhatsApp
```

---

# 🤖 Funcionalidades

## Chatbot Inteligente
- Conversa contextual
- Atendimento humanizado
- Memória de conversa
- Prompt engineering

---

## Captura de Leads
- Formulário de atendimento
- Validação de dados
- Registro automático

---

## Dashboard Administrativo
- Visualização de leads
- Estatísticas
- Métricas
- Exportação Excel

---

## Integração com IA
- Respostas automáticas
- Contextualização
- Base de conhecimento
- IA generativa

---

## Automação com n8n
- Webhooks
- Integrações
- Processamento automático
- Fluxos inteligentes

---

## SMTP Gmail
- Envio automático de emails
- Notificações internas
- Alertas de novos leads

---

# 📂 Estrutura do Projeto

```text
chatbot-psicologia/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── dados_clinica.json
├── base_conhecimento.txt
├── historico.txt
├── leads.csv
│
├── templates/
│   ├── index.html
│   ├── atendimento.html
│   ├── leads.html
│   └── obrigado.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
└── docs/
    ├── Relatorio_Tecnico.docx
    └── Apresentacao.pptx
```

---

# 🔐 Variáveis de Ambiente

Crie um arquivo:

```env
.env
```

Configure:

```env
GROQ_API_KEY= SUA_API_KEY

EMAIL_REMETENTE= seuemail@gmail.com
EMAIL_SENHA= suasenha

ADMIN_USER= admin
ADMIN_PASS= senha
```

---

# ⚙️ Instalação

## 1. Clonar repositório

```bash
git clone https://github.com/seuusuario/chatbot-psicologia.git
```

---

## 2. Entrar na pasta

```bash
cd chatbot-psicologia
```

---

## 3. Criar ambiente virtual

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando o Projeto

```bash
python app.py
```

Servidor:
```text
http://127.0.0.1:5000
```

---

# 🔑 Login Administrativo

Rota:
```text
/login
```

Acesso configurado via:
```env
ADMIN_USER
ADMIN_PASS
```

---

# 📊 Dashboard

Painel administrativo responsável por:

- Listagem de leads
- Métricas
- Estatísticas
- Exportação Excel

Rota:
```text
/leads
```

---

# 📤 Exportação Excel

O sistema exporta automaticamente:

```text
leads_export.xlsx
```

Utilizando:
- Pandas
- DataFrame
- OpenPyXL

---

# 🔗 Integração com n8n

Webhook utilizado:

```python
requests.post(
    "https://SEU_WEBHOOK_N8N",
    json=payload
)
```

O n8n permite:
- automações
- integração CRM
- WhatsApp
- workflows inteligentes

---

# 🧠 Funcionamento da IA

A IA utiliza:
- contexto personalizado
- engenharia de prompt
- histórico conversacional
- base de conhecimento clínica

Modelo:
```text
llama-3.3-70b-versatile
```

---

# 📧 Fluxo SMTP Gmail

```text
Flask
   ↓
SMTP Gmail
   ↓
Autenticação
   ↓
Envio Email
```

---

# 🔄 Fluxo Automatizado Completo

```text
Usuário envia mensagem
         ↓
Flask recebe requisição
         ↓
IA Groq responde
         ↓
Sistema detecta interesse
         ↓
Lead preenchido
         ↓
CSV atualizado
         ↓
Webhook enviado
         ↓
n8n processa automação
         ↓
Email disparado
         ↓
Dashboard atualizado
```

---

# 🛡️ Segurança

## Implementado
- Variáveis de ambiente
- Sessões Flask
- Login protegido
- Flask-Login

## Melhorias Futuras
- HTTPS
- Hash de senha
- PostgreSQL
- Rate limiting
- CSRF Protection

---

# 📌 APIs Utilizadas

| API | Finalidade |
|---|---|
| Groq API | IA generativa |
| OpenAI SDK | Comunicação LLM |
| Gmail SMTP | Envio email |
| n8n Webhook | Automação |
| WhatsApp Link API | Contato rápido |

---

# 📚 Conceitos Técnicos Aplicados

- Backend Web
- APIs REST
- IA Generativa
- Prompt Engineering
- Sessões Web
- Webhooks
- SMTP
- Automação
- Dashboard Analítico
- CSV/DataFrame
- Threads
- Integração HTTP

---

# 📈 Melhorias Futuras

- Banco PostgreSQL
- Redis
- Docker
- Deploy Cloud
- Integração WhatsApp API
- CRM completo
- Analytics IA
- Multiusuários

---

# 🎓 Aplicação Acadêmica

Projeto aplicável em:
- Engenharia de Software
- Sistemas Web
- Inteligência Artificial
- Automação de Processos
- Sistemas Clínicos
- Chatbots Inteligentes

---

# 👨‍💻 Autor

Desenvolvido por:

```text
Jader Gonçalves
```

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais.

---

# ⭐ Considerações Finais

Este sistema demonstra integração entre:

- Inteligência Artificial
- Backend Web
- Automação
- APIs
- Sessões
- SMTP
- Dashboards
- Engenharia de Prompt
- Arquitetura Web Moderna

Criando uma solução inteligente, escalável e moderna para clínicas de psicologia.