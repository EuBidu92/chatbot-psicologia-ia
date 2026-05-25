from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    send_file
)

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import threading
import pandas as pd
import csv
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)
if not GROQ_API_KEY:

    raise ValueError(
        "A variável de ambiente GROQ_API_KEY não foi definida."
    )

import json
from datetime import datetime

import smtplib
from email.mime.text import MIMEText

def enviar_email_lead(nome, whatsapp, email, motivo, preferencia, periodo):

    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
    EMAIL_SENHA = os.getenv("EMAIL_SENHA")

    destinatario = "eubidu92@gmail.com"

    assunto = "Novo Lead Captado"

    corpo = f"""
Novo lead recebido:

Nome: {nome}
WhatsApp: {whatsapp}
Email: {email}
Motivo: {motivo}
Preferência: {preferencia}
Período: {periodo}
"""

    msg = MIMEText(corpo)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        servidor.quit()

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print("Erro ao enviar e-mail:", e)

# =====================================
# CLIENTE GROQ
# =====================================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =====================================
# FLASK
# =====================================

app = Flask(__name__)
app.secret_key = "chatbot_psicologia_2026"

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id


ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# =====================================
# PALAVRAS DE CAPTAÇÃO DE LEADS
# =====================================

palavras_lead = [

    "agendar",
    "consulta",
    "atendimento",
    "terapia",
    "psicologo",
    "psicóloga",
    "psicologa",
    "psicanalista",
    "valor",
    "preço",
    "preco",
    "quanto custa",
    "marcar consulta",
    "quero atendimento"

]

# =====================================
# DADOS DA CLÍNICA
# =====================================

with open(
    "dados_clinica.json",
    "r",
    encoding="utf-8"
) as arquivo:

    dados = json.load(arquivo)

# =====================================
# BASE DE CONHECIMENTO
# =====================================

with open(
    "base_conhecimento.txt",
    "r",
    encoding="utf-8"
) as arquivo:

    base_conhecimento = arquivo.read()

# =====================================
# FUNÇÃO DE RESPOSTA
# =====================================

def responder(pergunta, historico):

    try:

        contexto = f"""
Você é a assistente virtual da clínica Saúde Mental Psicologia.

Base de conhecimento da clínica:

{base_conhecimento}

Informações da clínica:

Nome: {dados.get('nome', 'Saúde Mental Psicologia')}

Cidade: {dados.get('cidade', 'Salvador - BA')}

Especialidades:
{', '.join(dados.get('especialidades', []))}

Modalidades:
{', '.join(dados.get('modalidades', []))}

Regras:

- Responda de forma acolhedora.
- Seja objetiva.
- Não faça diagnósticos.
- Não substitua acompanhamento psicológico.
- Utilize prioritariamente as informações da base de conhecimento.
- Se a informação não estiver na base de conhecimento,
  informe educadamente que não possui essa informação específica e oriente a clicar no botão 
  'Falar no WhatsApp' para falar com um psicólogo ou psicanalista.
- Quando necessário, incentive a busca por atendimento profissional.
- Quando o usuário demonstrar interesse em iniciar atendimento,
  agendar consulta ou solicitar valores,
  oriente-o a clicar no botão 'Falar no WhatsApp'.
"""

        mensagens = [

            {
                "role": "system",
                "content": contexto
            }

        ]

        # Últimas mensagens da conversa
        for item in historico[-10:]:

            if item["tipo"] == "usuario":

                mensagens.append({

                    "role": "user",

                    "content": item["texto"]

                })

            elif item["tipo"] == "bot":

                mensagens.append({

                    "role": "assistant",

                    "content": item["texto"]

                })

        # Pergunta atual
        mensagens.append({

            "role": "user",

            "content": pergunta

        })

        resposta = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=mensagens,

            temperature=0.7,

            max_tokens=500

        )

        return resposta.choices[0].message.content

    except Exception as erro:

        print("ERRO GROQ:")
        print(erro)

        return (
            "Desculpe, estou temporariamente "
            "indisponível. Tente novamente "
            "em alguns instantes."
        )


# =====================================
# FORMULÁRIO DE ATENDIMENTO
# =====================================

@app.route("/atendimento")
def atendimento():

    return render_template(
        "atendimento.html"
    )


@app.route(
    "/salvar_lead",
    methods=["POST"]
)
def salvar_lead():

    nome = request.form["nome"]

    whatsapp = request.form["whatsapp"]

    email = request.form["email"]

    motivo = request.form["motivo"]

    preferencia = request.form["preferencia"]

    periodo = request.form["periodo"]

    # ==========================
    # VALIDAÇÕES
    # ==========================

    if len(nome.strip()) < 3:

        return """
        Nome inválido.
        <br><br>
        <a href='/atendimento'>Voltar</a>
        """

    if len(whatsapp.strip()) < 10:

        return """
        WhatsApp inválido.
        <br><br>
        <a href='/atendimento'>Voltar</a>
        """

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    # ==========================
    # CRIA O CSV SE NÃO EXISTIR
    # ==========================

    if not os.path.exists("leads.csv"):

        with open(
            "leads.csv",
            "w",
            encoding="utf-8-sig"
        ) as arquivo:

            arquivo.write(
                "Data,Nome,WhatsApp,Email,Motivo,Preferencia,Periodo\n"
            )

    # ==========================
    # SALVA O LEAD
    # ==========================

    with open(
        "leads.csv",
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        arquivo.write(
            f"{data},{nome},{whatsapp},{email},{motivo},{preferencia},{periodo}\n"
        )

    threading.Thread(
        target=enviar_email_lead,
        args=(nome, whatsapp, email, motivo, preferencia, periodo)
    ).start()

    link = gerar_link_whatsapp(nome, whatsapp)
    print(link)

    print("LEAD SALVO")
    print(os.path.abspath("leads.csv"))

    payload = {
        "nome": nome,
        "whatsapp": whatsapp,
        "email": email,
        "motivo": motivo,
        "preferencia": preferencia,
        "periodo": periodo,
        "data": data
    }

    try:
        resposta = requests.post(
    "https://bidu92.app.n8n.cloud/webhook/novo-lead",
    json=payload,
    timeout=5
)
        print("STATUS:", resposta.status_code)
        print("RESPOSTA:", resposta.text)

        print("Webhook enviado para n8n")
    except Exception as e:
        print("Erro ao enviar para n8n:", e)

    return render_template(
        "obrigado.html"
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USER and password == ADMIN_PASS:

            user = User(username)
            login_user(user)

            return redirect("/leads")

        return "Login inválido"

    return """
    <form method="POST">
        <input name="username" placeholder="Usuário">
        <input name="password" type="password" placeholder="Senha">
        <button type="submit">Entrar</button>
    </form>
    """

@app.route("/leads")
@login_required
def listar_leads():

    leads = []

    total = 0
    online = 0
    presencial = 0

    manha = 0
    tarde = 0
    noite = 0

    hoje = datetime.now().strftime("%d/%m/%Y")

    if os.path.exists("leads.csv"):

        with open("leads.csv", "r", encoding="utf-8-sig") as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:

                leads.append(linha)
                total += 1

                # Tipo de atendimento
                if linha["Preferencia"].lower() == "online":
                    online += 1
                elif linha["Preferencia"].lower() == "presencial":
                    presencial += 1

                # Período
                periodo = linha["Periodo"].lower()

                if "manhã" in periodo or "manha" in periodo:
                    manha += 1
                elif "tarde" in periodo:
                    tarde += 1
                elif "noite" in periodo:
                    noite += 1

    return render_template(
        "leads.html",
        leads=leads,
        total=total,
        online=online,
        presencial=presencial,
        manha=manha,
        tarde=tarde,
        noite=noite
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/exportar")
@login_required
def exportar():

    if not os.path.exists("leads.csv"):
        return "Nenhum lead encontrado."

    df = pd.read_csv("leads.csv", encoding="utf-8-sig")

    arquivo = "leads_export.xlsx"
    df.to_excel(arquivo, index=False)

    return send_file(arquivo, as_attachment=True)

@app.route("/limpar")
def limpar():

    session.pop(
        "historico_chat",
        None
    )

    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def inicio():

    if "historico_chat" not in session:

        session["historico_chat"] = [

            {
                "tipo": "bot",
                "texto":
                "Olá! Sou a assistente virtual da Saúde Mental Psicologia.\n\n"
                "Posso ajudar com:\n"
                "• Ansiedade\n"
                "• Depressão\n"
                "• Psicoterapia\n"
                "• Atendimento Online\n"
                "• Agendamento\n\n"
                "Como posso ajudar você hoje?"
            }

        ]

    if "mostrar_botao_lead" not in session:

        session["mostrar_botao_lead"] = False

    if request.method == "POST":

        pergunta = request.form["pergunta"]

        texto = pergunta.lower()

        for palavra in palavras_lead:

            if palavra in texto:

                session["mostrar_botao_lead"] = True

                break

        resposta = responder(
            pergunta,
            session["historico_chat"]
        )

        conversa = session["historico_chat"]

        conversa.append({
            "tipo": "usuario",
            "texto": pergunta
        })

        conversa.append({
            "tipo": "bot",
            "texto": resposta
        })

        session["historico_chat"] = conversa

        agora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        with open(
            "historico.txt",
            "a",
            encoding="utf-8"
        ) as arquivo:

            arquivo.write(
                f"[{agora}] Usuário: {pergunta}\n"
            )

            arquivo.write(
                f"[{agora}] Bot: {resposta}\n\n"
            )

    return render_template(
        "index.html",
        conversa=session["historico_chat"],
        mostrar_botao_lead=session["mostrar_botao_lead"]
    )

# =====================================
# FUNÇÕES AUXILIARES
# =====================================

def gerar_link_whatsapp(nome, whatsapp):

    mensagem = f"Olá! Recebemos seu contato, {nome}. Em breve vamos te responder 😊"

    return f"https://wa.me/{whatsapp}?text={mensagem}"

# =====================================
# INICIAR SERVIDOR
# =====================================

if __name__ == "__main__":

    print("APP INICIADO")
print(app.url_map)

app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )