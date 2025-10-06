from helpers.extensoes import *
from datetime import datetime
from slugify import slugify


class Desafio(db_real.Model):
    __tablename__ = 'desafios'
    id = db_real.Column(db_real.Integer, primary_key=True)
    titulo = db_real.Column(db_real.String(100), nullable=False)
    descricao = db_real.Column(db_real.Text, nullable=False)
    slug = db_real.Column(db_real.String(120), unique=True, nullable=False)
    criado_em = db_real.Column(db_real.DateTime, default=db_real.func.now())
    autor_id = db_real.Column(db_real.Integer, db_real.ForeignKey('usuario.id'), nullable=False)
    autor = db_real.relationship('Usuario', backref='desafios')
    nivel = db_real.Column(db_real.String(50), nullable=True)
    categoria = db_real.Column(db_real.String(50), nullable=True)
    estado = db_real.Column(db_real.Boolean, default=True)
    flags = db_real.relationship('Flag', backref='desafio', cascade='all, delete-orphan')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.slug and self.titulo:
            self.slug = slugify(self.titulo)
