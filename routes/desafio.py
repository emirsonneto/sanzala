import slugify
from helpers.extensoes import *
from models.desafios import Desafio
from models.flag import Flag, FlagValidada 
from helpers.forms import DesafioForm, FlagField
from sqlalchemy import func

desafio_bp = Blueprint('desafio_bp', __name__)


@desafio_bp.route('/desafios')
def lista_desafios():
    desafios = Desafio.query.all()
    mapa_visual = {
            'Sabedoria':    {'cor': 'roxo', 'icone': 'bi-journal-richtext'},
            'exploracao':   {'cor': 'azul', 'icone': 'bi-compass'},
            'treinamento':  {'cor': 'vermelho', 'icone': 'bi-eye'},
            'missao':       {'cor': 'verde', 'icone': 'bi-flag'},
            'aprendizado':  {'cor': 'azul', 'icone': 'bi-lightbulb'},
            }

    return render_template('desafios.html', desafios=desafios, mapa_visual=mapa_visual)


@desafio_bp.route('/desafio/<int:id>-<slug>')
@login_required
def ver_desafio(id, slug):
    desafio = Desafio.query.get_or_404(id)

    form = DesafioForm()

    # Preenche dinamicamente o form.flags
    form.flags.entries = []  # Limpa se já houver
    for flag in desafio.flags:
        flag_data = {'titulo': flag.titulo, 'valor': ''}
        form.flags.append_entry(flag_data)

    # Flags já validadas pelo usuário atual (opcional, para marcar como válidas)
    validadas = FlagValidada.query.filter_by(user_id=current_user.id, desafio_id=desafio.id).all()
    validadas_ids = {v.flag_id for v in validadas}

    return render_template(
        'visualizar_missao.html',
        desafio=desafio,
        form=form,
        flags_validadas=validadas_ids
    )


@desafio_bp.route('/desafio/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_desafio():
    form = DesafioForm()
    t = form.titulo.data

    # Garante sempre 5 campos de flag no GET
    if request.method == 'GET' and len(form.flags.entries) < 5:
        for _ in range(5 - len(form.flags.entries)):
            form.flags.append_entry()

    if form.validate_on_submit():
        novo_desafio = Desafio(
            titulo=t,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            nivel=form.nivel.data,
            slug=slugify.slugify(t),
            autor_id=current_user.id
        )

        # Salva só as flags preenchidas
        for flag_form in form.flags.entries:
            titulo = flag_form.form.titulo.data
            valor = flag_form.form.valor.data
            if titulo and valor:
                nova_flag = Flag(titulo=titulo, valor=valor)
                novo_desafio.flags.append(nova_flag)

        db_real.session.add(novo_desafio)
        db_real.session.commit()
        flash("Desafio cadastrado com sucesso!", "success")
        return redirect(url_for('desafio_bp.lista_desafios'))

    return render_template('novo_desafio.html', form=form)





@desafio_bp.route('/desafio/<int:id>/validar_flag', methods=['POST'])
@login_required
def validar_flag(id):
    desafio = Desafio.query.get_or_404(id)
    data = request.get_json()
    print("📥 JSON recebido:", data)

    flag_digitada = data.get('valor', '').strip()
    print("🧪 Flag enviada:", flag_digitada)

    if not flag_digitada:
        return jsonify({'success': False, 'mensagem': 'Flag não enviada.'})

    # Pegando todas as flags desse desafio
    flags_do_desafio = Flag.query.filter_by(desafio_id=desafio.id).all()
    print("🎯 Flags do banco:", [f.valor for f in flags_do_desafio])

    # Busca por flag correta ignorando maiúsculas e espaços
    flag_obj = next((f for f in flags_do_desafio if f.valor.strip().lower() == flag_digitada.lower()), None)

    if flag_obj:
        # Verifica se já validou
        ja_validou = FlagValidada.query.filter_by(
            user_id=current_user.id,
            flag_id=flag_obj.id
        ).first()

        if ja_validou:
            print("⚠️ Já validou essa flag.")
            return jsonify({'success': False, 'mensagem': '⚠️ Você já validou essa flag.'})

        # Salva a validação
        validada = FlagValidada(
            user_id=current_user.id,
            flag_id=flag_obj.id,
            desafio_id=desafio.id
        )
        db_real.session.add(validada)
        current_user.pontos += 10
        db_real.session.commit()
        print("✅ Flag validada com sucesso!")

        return jsonify({'success': True, 'mensagem': '✅ Flag correta! +10 pontos'})

    print("❌ Flag incorreta (não encontrada mesmo ignorando maiúsculas).")
    return jsonify({'success': False, 'mensagem': '❌ Flag incorreta.'})




@desafio_bp.route('/desafio/<slug>')
@login_required
def missao(slug):
    missao = Desafio.query.filter_by(slug=slug).first_or_404()
    return render_template(f'{slug}.html', missao=missao)


@desafio_bp.route('/vale-do-rift/rift-html')
@login_required
def rift_html():
    return render_template("rift_html.html")


@desafio_bp.route('/origen-de-kemet/kemet_css')
@login_required
def kemet_css():
    return render_template("kemet2.html")



@desafio_bp.route('/tesouro-de-timbuktu/kembuktu2')
@login_required
def timbuktu():
    return render_template("timbuktu2.html")

@desafio_bp.route('/reino-do-ndongo')
@login_required
def ndongo():
    return render_template("reino-do-ndongo.html")

@desafio_bp.route('/reino-do-ndongo/ndongo2')
@login_required
def ndongo2():
    return render_template("ndongo2.html")

@desafio_bp.route('/mbamza-kazul/kazul')
@login_required
def robots():
    return render_template("kazul.html")


@desafio_bp.route('/mbamza-kazul/robots.txt')
def robotsx():
    conteudo = """User-agent: *
    Disallow: /admin
    Disallow: /files
    Disallow: /user
    Disallow: /backup.zip
    Disallow: /nbanza-kongo
    Dissalow: /secreto
    """
    return Response(conteudo, mimetype='text/plain')


@desafio_bp.route('/mbamza-kazul/sitemap.xml')
def sitemap():
    conteudo = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>http://localhost:5000/home</loc>
      </url>
      <url>
        <loc>http://localhost:5000/contacto</loc>
      </url>
      <url>
        <loc>http://localhost:5000/user?admin=true</loc>
      </url>
      <url>
        <loc>http://localhost:5000/mbamba-kazul/assets></loc>
      </url>
    </urlset>"""
    return Response(conteudo, mimetype='application/xml')


@desafio_bp.route('/mbamza-kazul/admin')
def admin():
    return "🔒 Área restrita. Acesso negado.", 403

@desafio_bp.route('/muralha-de-mbamza-kazul/backup.zip')
def backup():
    return "📦 Arquivo zip corrompido ou removido.", 404

@desafio_bp.route('/mbamza-kazul/user')
def userr():
    return "👤 Bem-vindo, administrador? Este parâmetro parece suspeito...", 200

@desafio_bp.route('/mbamza-kazul/files', methods=['GET','HEAD','POST'])
def files():
	error= None
	if request.method == "POST" and request.form['files'] == "a":
		return render_template("africa.html")
	return render_template("files.html", error="precisa de outros methods http")


@desafio_bp.route('/mbamza-kazul/secreto')
def secreto():
	return """Continue mapeando e enumerando ...
		3c0{enumerar_info_e_sempre_importante_para_uma_flag}"""


@desafio_bp.route('/mbamza-kazul/assets')
def assets():
        return """ <p>boas nao te esquecas dos verbis http mapeando e enumerando 
                3c0{enumerar_sempre_olhar_tudo_para_pegar_tudo} </p>
	      """
