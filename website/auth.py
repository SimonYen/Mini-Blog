from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('登录成功。', category='success')
                if request.form.get('remember') == 'on':
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('密码错误！', category='error')
        else:
            flash('邮箱不存在！', category='info')
    return render_template('login.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('邮箱已被注册！', category='error')
        elif password != password_confirm:
            flash('重复密码不一致！', category='error')
        elif len(username) < 2:
            flash('用户名长度太短了！', category='error')
        elif len(password) < 5:
            flash('密码必须大于5个字符！', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password=password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('成功创建账号。', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
