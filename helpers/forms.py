from helpers.extensoes import *


class FormLogin(FlaskForm):
  email = StringField('Email', validators=[
      DataRequired(message="Preencha o email."),
      Email(message="Email inválido.")
  ])

  senha = PasswordField('Senha', validators=[
      DataRequired(message="Informe a senha.")
  ])

  termos = BooleanField('Aceito os termos', validators=[
      DataRequired(message="Você deve aceitar os termos.")
  ])

  submit = SubmitField('Entrar')

class FormRegistro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    origem = SelectField('Aldeia / Clã', choices=[
        ('leoes', 'Clã dos Leões'),
        ('grios', 'Aldeia dos Griôs'),
        ('guardioes', 'Guardião das Chamas')
    ], validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    csenha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    pin = StringField('PIN', validators=[DataRequired()])
    avatar = SelectField('Avatar / Personagem', choices=[
        ('nzinga', 'Nzinga'),
        ('mutu', 'Mutu-ya-Kevela'),
        ('kibinda', 'Kibinda'),
        ('guardiao', 'Guardião Ancestral')
    ], validators=[DataRequired()])
    termos = BooleanField('Aceito os termos', validators=[DataRequired()])
    submit = SubmitField('Criar Conta')


class FormVerificarConta(FlaskForm):
  email  =  StringField('Email', validators=[DataRequired(), Email()])
  pin    =  StringField('PIN', validators=[DataRequired(), Length(min=1, max=4)])
  submit = SubmitField('Verificar')

class FormRedifinir(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[DataRequired()])
    csenha = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('senha', message='As senhas não coincidem.')
    ])
    submit = SubmitField('Atualizar Senha')

class FormPost(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    conteudo = TextAreaField("Conteúdo", validators=[DataRequired()])
    submit = SubmitField("Publicar")


class FormComentario(FlaskForm):
    conteudo = TextAreaField("Comentário", validators=[DataRequired()])
    submit = SubmitField("Comentar")



class FlagField(FlaskForm):
    titulo = StringField("Título", validators=[Optional()])
    valor = StringField("Valor", validators=[Optional()])



class DesafioForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    categoria = SelectField("Categoria", choices=[('sabedoria', 'Sabedoria'), ('treinamento', 'Treinamento'),('aprendizado', 'Aprendizado'),('ancestral', 'Ancestral'),('exploracao', 'Exploração'), ('misterio', 'Misterio')])
    nivel = SelectField("Nível", choices=[('Aprendiz','Aprendiz'), ('Aldeao','Aldeao'),('Guardiao', 'Guardiao'),('Anciao', 'Anciao'),('Ancestral','Ancestral')])
    flags = FieldList(FormField(FlagField), min_entries=1, max_entries=5)
    submit = SubmitField("Cadastrar")
