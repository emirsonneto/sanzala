from helpers.extensoes import *
from models.post import Post


class Usuario(UserMixin,db_real.Model):
    __tablename__ = 'usuario' 
    id = db_real.Column(db_real.Integer, primary_key=True)
    nome = db_real.Column(db_real.String(150), nullable=False, unique=True)
    email = db_real.Column(db_real.String(150), nullable=False, unique=True)
    origem = db_real.Column(db_real.String(150), nullable=False) 
    senha_hash = db_real.Column(db_real.String(1050), nullable=False)
    pin_hash = db_real.Column(db_real.String(1050), nullable=False)
    avatar = db_real.Column(db_real.String(250), nullable=False)
    pontos = db_real.Column(db_real.Integer, default=0)
    posts = db_real.relationship('Post', back_populates='autor', cascade='all, delete')
    comentarios = db_real.relationship('Comentario', back_populates='autor', cascade="all, delete-orphan")
    is_admin = db_real.Column(db_real.Boolean, default=False)


    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def get_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


    def set_pin(self, pin):
        self.pin_hash = generate_password_hash(pin)

    def get_pin(self, pin):
        return check_password_hash(self.pin_hash, pin)


    def adicionar_pontos(self, quantidade):
        self.pontos += quantidade
        db_real.session.commit()

    @property
    def titulo(self):
        if self.pontos < 100:
            return "Aldeão"
        elif self.pontos < 200:
            return "Aprendiz"
        elif self.pontos < 500:
            return "Guardião"
        elif self.pontos < 1000:
            return "Escriba"
        else:
            return "Mestre"



