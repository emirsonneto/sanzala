from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import current_user, login_required, logout_user, login_user
from flask_wtf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,FieldList,BooleanField,TextAreaField, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from flask import Blueprint, render_template
from flask import redirect, url_for, flash, request, session , jsonify, Blueprint,Response, make_response
from flask_wtf.csrf import generate_csrf
# Inicializa as extensões
db_real = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
