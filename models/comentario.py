from helpers.extensoes import *
from datetime import datetime

class Comentario(db_real.Model):
    __tablename__ = "comentario"

    id = db_real.Column(db_real.Integer, primary_key=True)
    conteudo = db_real.Column(db_real.Text, nullable=False)
    data_criacao = db_real.Column(db_real.DateTime, default=datetime.utcnow)

    autor_id = db_real.Column(db_real.Integer, db_real.ForeignKey("usuario.id"), nullable=False)
    post_id = db_real.Column(db_real.Integer, db_real.ForeignKey("post.id"), nullable=False)

    autor = db_real.relationship("Usuario", back_populates="comentarios")
    post = db_real.relationship("Post", back_populates="comentarios")