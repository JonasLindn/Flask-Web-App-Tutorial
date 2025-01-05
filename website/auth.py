from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Anmeldung erfolgreich!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Falsches Passwort, bitte erneut versuchen.', category='error')
        else:
            flash('Diese Email existiert nicht.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    return render_template("new_project.html", user=current_user)


@auth.route('/project_info', methods=['GET', 'POST'])
@login_required
def project_info():
    return render_template("project_info.html", user=current_user)


@auth.route('/rahmenbedingungen', methods=['GET', 'POST'])
@login_required
def rahmenbedingungen():
    return render_template("rahmenbedingungen.html", user=current_user)


@auth.route('/priority', methods=['GET', 'POST'])
@login_required
def priority():
    return render_template("priority.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Diese Email existiert bereits.', category='error')
        elif len(email) < 4:
            flash('Email muss länger als 3 Zeichen sein.', category='error')
        elif len(first_name) < 2:
            flash('Vorname muss länger als 1 Zeichen sein.', category='error')
        elif password1 != password2:
            flash('Passwörter stimmen nicht überein.', category='error')
        elif len(password1) < 7:
            flash('Das Passwort muss mindestens eine länge von 7 Zeichen besitzen.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account erstellt!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
