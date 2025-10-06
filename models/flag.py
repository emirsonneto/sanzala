from helpers.extensoes import *
from datetime import datetime


class Flag(db_real.Model):
    __tablename__ = 'flags'

    id = db_real.Column(db_real.Integer, primary_key=True)
    titulo = db_real.Column(db_real.String(100))
    valor = db_real.Column(db_real.String(200), nullable=False)

    desafio_id = db_real.Column(db_real.Integer, db_real.ForeignKey('desafios.id'), nullable=False)


class FlagValidada(db_real.Model):
    __tablename__ = 'flags_validadas'

    id = db_real.Column(db_real.Integer, primary_key=True)
    user_id = db_real.Column(db_real.Integer, db_real.ForeignKey('usuario.id'), nullable=False)
    desafio_id = db_real.Column(db_real.Integer, db_real.ForeignKey('desafios.id'), nullable=False)
    flag_id = db_real.Column(db_real.Integer, db_real.ForeignKey('flags.id'), nullable=False)
    timestamp = db_real.Column(db_real.DateTime, default=datetime.utcnow)

    usuario = db_real.relationship('Usuario', backref='flags_validadas')
    desafio = db_real.relationship('Desafio', backref='flags_validadas')
    flag = db_real.relationship('Flag', backref='validações')
