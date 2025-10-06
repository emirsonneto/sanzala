from helpers.extensoes import *


class ComentarioFake(db_real.Model):
    __tablename__ = "comentarios_fake"
    __blind_key__ = "fake"
    autor= db_real.Column(db_real.Text)
    comentario=db_real.Column(db_real.Text)

