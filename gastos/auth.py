from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.monthly'))
            else:
                flash('Usuário ou senha incorretos', category='error')
        else:
            flash('Usuário ou senha incorretos', category='error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))