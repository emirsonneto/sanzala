from helpers.extensoes import *
from models.user import Usuario


public = Blueprint('public', __name__)

@public.route('/')
def home():
    return render_template("home.html")


@public.route('/termos')
def termos():
    return render_template("termos.html")

@public.route('/ancestrais')
def ver():
    total = 100
    return render_template("ancestral.html", total=total)


