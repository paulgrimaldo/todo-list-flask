from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from app.forms.login_form import AuthForm
from app.db.firestore_service import get_user, register_user
from ..models.User import UserData, User


@auth.route('/login', methods=['GET'])
def login():
    if _is_authenticated():
        return redirect(url_for('todos.index'))

    login_form = AuthForm()

    context = {
        'login_form': login_form
    }

    return render_template('login.html', **context)


@auth.route('/sign_in', methods=['POST'])
def sign_in():
    login_form = AuthForm(request.form)

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            if check_password_hash(user_doc.to_dict()['password'], password):
                user_data = UserData(username, password)
                user = User(user_data)

                login_user(user)

                session['username'] = username

                flash("Welcome {} !".format(username))

                return redirect('/')
            else:
                flash('Invalid password')
        else:
            flash('User not found')

    return redirect('login')


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Session closed')
    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET" and _is_authenticated():
        return redirect(url_for('todos.index'))

    signup_form = AuthForm()

    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            hashed_password = generate_password_hash(password)

            user_data = UserData(username, hashed_password)

            register_user(user_data)

            user = User(user_data)

            login_user(user)

            flash("Welcome {} !".format(username))

            return redirect(url_for('index'))
        else:
            flash('Username already in use')

    return render_template('signup.html', **context)


def _is_authenticated():
    return current_user.is_authenticated
