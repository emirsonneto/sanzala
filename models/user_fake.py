from helpers.extensoes import *


class UsuarioFake(db_real.Model):
    __bind_key__ = 'fake'
    __tablename__ = 'usuario_fake'
    id = db_real.Column(db_real.Integer, primary_key=True)
    nome = db_real.Column(db_real.String(100))
    email = db_real.Column(db_real.String(100))
    senha = db_real.Column(db_real.String(100))  # texto plano
