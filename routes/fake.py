from helpers.utils import *
from os import error
from helpers.extensoes import *
from models.produtos_fake import ProdutoFake
from models.user_fake import UsuarioFake
from sqlalchemy import text


bp_fake = Blueprint('fake', __name__)


@bp_fake.route('/criar_produtos', methods=['GET', 'POST'])
def criar_produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        novo_produto = ProdutoFake()
        novo_produto.nome = nome
        novo_produto.preco = preco
        novo_produto.descricao = descricao
        db_real.session.add(novo_produto)
        db_real.session.commit()
        return redirect(url_for('fake.loja'))
    return render_template('criar_produtos.html')


@bp_fake.route('/criar_user', methods=['GET', 'POST'])
def criar_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        novo_user = UsuarioFake()
        novo_user.nome = nome
        novo_user.email = email
        novo_user.senha = senha
        db_real.session.add(novo_user)
        db_real.session.commit()
        return redirect(url_for('fake.login_fake'))
    return render_template('criar_user.html')


@bp_fake.route('/login_fake', methods=['GET', 'POST'])
def login_fake():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = UsuarioFake.query.filter_by(email=email, senha=senha).first()

        if user:
            session_id = str(user.id)
            # session[session_id] = user.id
            # session['email']=user.email
            # session['nome'] =user.nome
            resposta = make_response(
                redirect(
                    url_for(
                        "fake.conta_fake",
                        sid=session_id)))
            # resposta.set_cookie("session_id", session_id)
            return resposta
        else:
            return render_template(
                'login_fake.html',
                error='Credenciais inválidas')
    return render_template('login_fake.html')


@bp_fake.route('/fake_sair')
def fake_sair():
    # Limpa toda a sessão
    session.clear()

    # Redireciona para a rota de login
    resposta = redirect(url_for('fake.login_fake'))
    # Remove o cookie 'user_id' também (se usado)
    resposta.set_cookie('user_id', '', expires=0)

    return resposta


@bp_fake.route('/loja_fake')
def loja():
    produtos = ProdutoFake.query.all()
    categorias = {
        'Vestuário': [],
        'Comida': [],
        'Eletrônicos': [],
        'Outros': []
    }
    for p in produtos:
        nome_lower = p.nome.lower()
        if any(
            k in nome_lower for k in [
                'camisa',
                'calça',
                'sapato',
                'blusa',
                'macacao',
                'vestido',
                'chapeu',
                'tenis',
                'bota']):
            categorias['Vestuário'].append(p)
        elif any(k in nome_lower for k in ['hamburguer', 'pizza', 'batata', 'arroz', 'feijão', 'carne', 'frango', 'peixe', 'ovo', 'leite', 'queijo', 'pão', 'bolo', 'biscoito', 'chocolate', 'sorvete', 'suco', 'refrigerante']):
            categorias['Comida'].append(p)
        elif any(k in nome_lower for k in ['notebook', 'celular', 'computador', 'telefone', 'tablet', 'televisao', 'relogio']):
            categorias['Eletrônicos'].append(p)
        else:
            categorias['Outros'].append(p)

    return render_template('loja_fake.html', categorias=categorias)


@bp_fake.route('/conta_fake')
def conta_fake():
    # Recupera o ID de sessão inseguro
    sid = request.args.get('sid')
    # Busca o usuário pelo nome
    user = UsuarioFake.query.filter_by(id=str(sid)).first()
    if not user:
        return 'Usuário não encontrado', 404

    return render_template('conta_fake.html', user=user)


@bp_fake.route('/buscar_produto', methods=['GET', 'POST'])
def buscar_produtos():
    resultado = None
    erro = None

    if request.method == 'POST':
        termo = request.form['termo']

        sql = text(
            f" SELECT * FROM produtos_fake WHERE nome = '{termo}' ORDER BY id ")

        try:

            conn = db_real.get_engine(bind='fake').connect()
            resultado = conn.execute(sql).fetchall()
        except Exception as e:
            erro = str(e)

    return render_template(
        'buscar_produto.html',
        resultado=resultado,
        erro=erro)


@bp_fake.route('/buscar_outros')
def buscar_outros():
    termo = request.args.get('termo', '')
    resultado = []
    erro = None

    try:
        sql = text(
            f" SELECT * FROM produtos_fake WHERE nome = '{termo}' ORDER BY id ")
        conn = db_real.get_engine(bind='fake').connect()
        resultado = conn.execute(sql).fetchall()
    except Exception as e:
        erro = str(e)

    return render_template(
        "buscar_outros.html",
        termo=termo,
        resultado=resultado,
        erro=erro)


@bp_fake.route('/login_sqli', methods=['GET', 'POST'])
def login_sqli():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')

# VULNERÁVEL: interpolação direta na SQL
        sql = text(
            f"SELECT * FROM usuario_fake WHERE email ='{email}' AND senha ='{senha}' ")

        try:
            conn = db_real.get_engine(bind='fake').connect()
            # pyright: ignore[reportPossiblyUnboundVariable]
            resultado = conn.execute(sql).fetchone()
            if resultado:
                return render_template(
                    "conta_fake.html", user=resultado, id=resultado.id)
            else:
                return render_template(
                    'login_sqli.html', error='Credenciais inválidas')
        except Exception as e:
            return e
        return render_template(
            'login_sqli.html',
            error='Credenciais inválidas')
    return render_template('login_sqli.html')


@bp_fake.route("/login_loja", methods=["GET", "POST"])
def login_loja():
    if request.method == "POST":
        email = request.form.getlist("email")
        senha = request.form.get("senha")

        # nome = request.form.get("nome")
        # role = request.args.get("role", "user")  # <- Ponto vulnerável!
        user = UsuarioFake.query.filter_by(email=email[0], senha=senha).first()
        if user:

            return redirect(
                url_for(
                    "fake.portal",
                    user=user.nome,
                    email=user.email))

        return render_template(
            "login_loja.html",
            erro="email ou senha errado!")
    return render_template("login_loja.html")


@bp_fake.route('/portal_sair')
def portal_sair():
    # Limpa toda a sessão
    session.clear()

    # Redireciona para a rota de login
    resposta = redirect(url_for('fake.login_loja'))

    return resposta


@bp_fake.route("/portal/")
def portal():
    if "nome" not in session:
        return redirect(url_for("fake.login_loja"))

    email = request.args.getlist('email')
    nome = request.args.get('nome')
    return render_template("portal.html", email=email)


@bp_fake.route('/outra_conta_fake')
def outra_conta_fake():
    # Recupera o ID de sessão inseguro
    sid = request.args.get('sid')
    cookie_session = request.cookies.get("cookie_session")
    if not sid or sid not in session:
        return 'Acesso negado', 403

    # Decodifica o nome de usuário a partir do session_id
    try:
        uid = session.get(sid)
    except KeyError:
        return 'Sessão inválida', 403

    user = UsuarioFake.query.filter_by(id=str(sid)).first()
    if not user:
        return 'Usuário não encontrado', 404

    # Valida se o cookie pertence ao user logado
    if cookie_session != rot13(user.nome):
        return 'Acesso negado', 403

    return render_template(
        'outra_conta_fake.html',
        user=user,
        cookie_session=cookie_session,
        uid=uid
    )


@bp_fake.route('/outro_login_fake', methods=['GET', 'POST'])
def outro_login_fake():

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = UsuarioFake.query.filter_by(email=email, senha=senha).first()

        if user:
            session_id = str(user.id)
            cookie_session = rot13(user.nome)
            session[session_id] = user.id
            session['email'] = user.email
            session['nome'] = user.nome
            resposta = make_response(
                redirect(
                    url_for(
                        "fake.outra_conta_fake",
                        sid=session_id)))
            resposta.set_cookie("cookie_session", cookie_session)
            return resposta
        else:
            return render_template(
                'outro_login_fake.html',
                error='Credenciais inválidas')
    return render_template('outro_login_fake.html')
