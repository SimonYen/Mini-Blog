from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import db
from .models import Post

views = Blueprint("views", __name__)


@views.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/my_posts')
@login_required
def my_posts():
    posts=Post.query.filter_by(author=current_user.id).all()
    return render_template('home.html', user=current_user, posts=posts)



@views.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('ckeditor')
        if not content:
            flash('帖子内容为空！', category='error')
        else:
            new_post = Post(title=title, content=content,
                            author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('帖子创建成功。', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)


@views.route('/view_post/<id>')
def view_post(id):
    p = Post.query.filter_by(id=id).first()
    return render_template('view_post.html', post=p , user=current_user)

@views.route('/motify_post/<id>', methods=['POST', 'GET'])
@login_required
def motify_post(id):
    p = Post.query.filter_by(id=id).first()
    if request.method=='POST':
        if p.author!=current_user.id:
            flash('你无权修改他人的帖子！')
        else:
            p.title = request.form.get('title')
            p.content = request.form.get('ckeditor')
            db.session.commit()
            flash('帖子修改成功。')
            return redirect(url_for('views.view_post',id=p.id))
    return render_template('motify_post.html',post=p,user=current_user)



@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    p = Post.query.filter_by(id=id).first()
    if not p:
        flash('所删除的帖子不存在！', category='info')
    else:
        if p.author != current_user.id:
            flash('你无权限删除别人的帖子！', category='error')
        else:
            db.session.delete(p)
            db.session.commit()
            flash('删除成功。', category='sucess')
            return redirect(url_for('views.home'))


@views.route('/about')
def about():
    return render_template('about.html', user=current_user)
