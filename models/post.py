from helpers.extensoes import *
from datetime import datetime



class Post(db_real.Model):
    id = db_real.Column(db_real.Integer, primary_key=True)
    titulo = db_real.Column(db_real.String(100), nullable=False)
    conteudo = db_real.Column(db_real.Text, nullable=False)
    data_criacao = db_real.Column(db_real.DateTime, default=datetime.utcnow)
    icone = db_real.Column(db_real.String(10), default=lambda: random.choice(icons))
    autor_id = db_real.Column(db_real.Integer, db_real.ForeignKey('usuario.id'), nullable=False)
    autor = db_real.relationship('Usuario', back_populates='posts')
    comentarios = db_real.relationship('Comentario', back_populates='post', cascade="all, delete-orphan")

