from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user
from flask_login import login_required

from werkzeug.urls import url_parse

from app import app
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template(
        'user.html',
        title="Profile",
        user=user,
        posts=user.posts
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Get index"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    """Post register"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))

    """Get register"""
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Get part if user authorized"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    """Post part if user send form"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')  # get with params next
        if not next_page or url_parse(next_page).netloc != '':  # netloc - domen
            next_page = url_for('index')
        return redirect(next_page)

    """"Get part user not auth."""
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
