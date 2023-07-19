from flask import Blueprint, render_template , request, flash , redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
 

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user: 
            if check_password_hash(user.password, password):
                flash('Login feito!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha está errada, tente novamente!', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("login.html",user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', "POST"]) 
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email já existe', category='error')
        elif len(email) < 4:
            flash('email precisa ter mais que 4 letras.', category='error')
        elif len(first_name) < 2:
            flash('Nome precisa ter mais que 2 letras.', category='error')
        elif Password1 != Password2:
            flash('Senhas não combinam', category='error')
        elif len(Password1) < 4:
            flash('Senha precisa ter mais que 4 caracteres.', category='error')
        else:
            new_user = User(email=email,first_name = first_name, password=generate_password_hash(Password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Conta criada!.', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user = current_user)


