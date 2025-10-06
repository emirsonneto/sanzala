
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from helpers.extensoes import db_real, login_manager, csrf, mail
from models.user import Usuario
from models.control_user import SecureModelView
from models.user_fake import UsuarioFake
from models.produtos_fake import ProdutoFake
from models.desafios import Desafio
from models.flag import Flag, FlagValidada
from routes.auth import auth
from routes.public import public
from routes.fake import bp_fake
from routes.desafio import desafio_bp
from flask_wtf.csrf import generate_csrf

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("DB_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")

# Banco fake
app.config['SQLALCHEMY_BINDS'] = {
    'fake': os.getenv("DB_URL_FAKE")
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email config (⚠️ use variáveis de ambiente em produção!)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='eden@gmail.com',
    MAIL_PASSWORD='adao'
)

# Inicializar extensões
db_real.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
csrf.init_app(app)
mail.init_app(app)

# Admin
admin = Admin(app, name="Painel", template_mode="bootstrap4")
admin.add_view(SecureModelView(Usuario, db_real.session))
admin.add_view(SecureModelView(UsuarioFake, db_real.session))
admin.add_view(SecureModelView(ProdutoFake, db_real.session))
admin.add_view(SecureModelView(Flag, db_real.session))
admin.add_view(SecureModelView(FlagValidada, db_real.session))
admin.add_view(SecureModelView(Desafio, db_real.session))

# Blueprints
app.register_blueprint(auth)
app.register_blueprint(public)
app.register_blueprint(desafio_bp)
app.register_blueprint(bp_fake)

# Criar tabelas

with app.app_context():
    db_real.create_all()  # cria tabelas no banco principal
   # db_real.create_all(bind='fake')  # cria tabelas no banco fake

"""class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
"""

# Autenticação
@login_manager.user_loader
def user_loader(user_id):
    return Usuario.query.get(int(user_id))

# Página 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# CSRF Token para formulários
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

# Roda o app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
