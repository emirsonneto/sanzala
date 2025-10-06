import os, random
from helpers.extensoes import *
from helpers.forms import *
from models.user import Usuario
from models.desafios import Desafio
from models.post import Post
from models.comentario import Comentario
from helpers.utils import *



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.get_senha(form.senha.data):
            login_user(user)
            return redirect(url_for('public.home'))
        else:
            flash('Login falhou. Verifique seu nome e senha.')
            return redirect(url_for('auth.login',form=form))
    return render_template('login.html', form=form)    


@auth.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    form = FormPost()

    # Paginação segura
    page = max(1, request.args.get('page', 1, type=int))
    per_page = 4  # ← Exibe 4 posts por página

    if form.validate_on_submit():
        novo_post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            autor=current_user,
            icone=random.choice(icones)
        )
        db_real.session.add(novo_post)
        db_real.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('auth.blog'))

    # Pagina os posts do mais novo para o mais antigo
    paginacao = Post.query.order_by(Post.data_criacao.desc()).paginate(page=page, per_page=per_page)
    posts = paginacao.items

    return render_template('blog.html', form=form, posts=posts, paginacao=paginacao)



@auth.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def ver_post(id):
    post = Post.query.get_or_404(id)
    form = FormComentario()
    if form.validate_on_submit():
        comentario = Comentario(
            conteudo=form.conteudo.data,
            autor=current_user,
            post=post
        )
        db_real.session.add(comentario)
        db_real.session.commit()
        flash('Comentário publicado!', 'success')
        return redirect(url_for('auth.ver_post', id=post.id))

    return render_template('blog_comentar.html', post=post, form=form)




@auth.route('/registro', methods=['GET','POST'])
def registro():
    
    form = FormRegistro()
    avatares = listar_avatars()
    form.avatar.choices = [(a, os.path.basename(a)) for a in avatares]
  
    if form.validate_on_submit():
        nome = form.nome.data
        origem = form.origem.data
        avatar = form.avatar.data
        email = form.email.data  
        user_email = Usuario.query.filter_by(email=email).first()
        if user_email:
            flash('email de usuário já existe. Escolha outro.')
            return redirect(url_for('auth.registro'))
        novo_user = Usuario()
        novo_user.nome = nome
        novo_user.email = email
        novo_user.origem = origem
        novo_user.avatar = avatar
        novo_user.set_senha(form.senha.data)
        novo_user.set_pin(form.pin.data)
        db_real.session.add(novo_user)
        db_real.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('registro.html', form=form)


@auth.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))


@auth.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    
    form = FormVerificarConta()
    if form.validate_on_submit():
        email = form.email.data
        pin = form.pin.data
        user = Usuario.query.filter_by(email=email).first()
        if user and user.get_pin(form.pin.data):
            #token = gerar_token(email)
            #enviar_email_redefinicao(email, token)
            flash('Um link para redefinir a senha foi enviado para seu e-mail.')
            session['email'] = email
            return redirect(url_for('auth.redifinir', email=email))
        else:
            flash('E-mail não encontrado.')
    return render_template('recuperar.html', form=form)


@auth.route('/redefinir_senha', methods=['GET', 'POST'])
def redifinir():
    form = FormRedifinir()
    email = session.get('email')
    #email = verificar_token(token)
    if not email:
        flash('Sessão expirada ou e-mail ausente. Tente novamente.')
        return redirect(url_for('auth.recuperar'))

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        flash('Usuário não encontrado.')
        return redirect(url_for('auth.recuperar'))

    if form.validate_on_submit():
        user.set_senha(form.senha.data)
        db_real.session.commit()
        session.pop('email', None)  # Remove o email da sessão
        flash('Senha redefinida com sucesso.')
        return redirect(url_for('auth.login'))

    return render_template("redifinir.html", form=form)
        
            