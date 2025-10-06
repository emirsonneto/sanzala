from helpers.extensoes import *


class ProdutoFake(db_real.Model):
  __bind_key__ = 'fake'
  __tablename__ = 'produtos_fake'
  id = db_real.Column(db_real.Integer, primary_key=True)
  nome = db_real.Column(db_real.String(100))
  preco = db_real.Column(db_real.String(50)) 
  descricao = db_real.Column(db_real.Text)

  def __repr__(self):
      return f"<ProdutoFake {self.nome}>"
    