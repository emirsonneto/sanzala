
from flask_mail import Message
from flask import url_for
from helpers.extensoes import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import os
from flask import url_for
import codecs


def enviar_email_redefinicao(email, token):
    link = url_for('auth.redifinir', token=token, _external=True)
    msg = Message('Redefinir sua senha', recipients=[email])
    msg.body = f'''Olá,

Para redefinir sua senha, clique no link abaixo:

{link}

Se você não solicitou isso, ignore este e-mail.
'''
    mail.send(msg)


def gerar_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='token-redefinir-senha')

def verificar_token(token, tempo_expiracao=300):  # 10 minutos por padrão
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='token-redefinir-senha', max_age=tempo_expiracao)
        return email
    except Exception:
        return None
        

def listar_avatars():
    caminho = os.path.join('static', 'avatars')
    arquivos = sorted(os.listdir(caminho))

    # Filtra apenas SVGs (ou PNGs se quiser)
    avatars = [
        url_for('static', filename=f'avatars/{nome}')
        for nome in arquivos
        if nome.endswith('.svg')
    ]
    return avatars




icones = [
  "🌀",  # Energia ancestral
  "🌌",  # Cosmos
  "🗝️",  # Chave dos segredos
  "📜",  # Manuscrito
  "🧬",  # Genética ancestral
  "⚔️",  # Luta, resistência
  "🔥",  # Rebelião, espírito
  "👁️",  # Visão do griot
  "💡",  # Iluminação
  "🧠",  # Sabedoria
  "⛓️",  # Correntes quebradas
  "🛡️",  # Guardião, proteção
  "🪶",  # Tradição oral
  "🔮",  # Profecia
  "🌿",  # Sabedoria natural
  "🛰️",  # Tecnologia
  "💀",  # Memória dos ancestrais
  "🎭",  # Identidade oculta
  "📡",  # Conexão digital
  "🕯️",  # Luz no escuro
  "🌍",  # África
  "🪬",  # Amuleto
  "⏳",  # Tempo
  "🧱",  # Construção, resistência
  "📀",  # Dados antigos
  "🎮",  # Hacker/CTF
  "🪐",  # Mistério cósmico
  "🔓",  # Quebra de sistemas
  "🎙️",  # Voz do povo
  "🧭"   # Caminho da jornada
] 

def rot13(text):
    return codecs.encode(text, 'rot_13')
