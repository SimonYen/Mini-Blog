import os
from flask import Blueprint, flash, redirect, render_template, request, url_for,send_file
from flask_login import current_user, login_required
from . import db,UPLOAD_FOLDER
from .models import Post,File

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



@views.route('/netpan')
@login_required
def netpan_home():
    return render_template('netpan.html',user=current_user)

@views.route('/netpan_upload',methods=['POST','GET'])
@login_required
def netpan_upload():
    if request.method == 'POST':
        file=request.files['file']
        if file:
            f=File(name=file.filename,owner=current_user.id)
            file.save(os.path.join(UPLOAD_FOLDER,file.filename))
            db.session.add(f)
            db.session.commit()
            flash('上传成功。')
        else:
            flash('文件为空！文件传输过程失败！')
    return render_template('netpan_upload.html',user=current_user)

@views.route('/netpan_control.html')
@login_required
def netpan_control():
    files=File.query.filter_by(owner=current_user.id).all()
    return render_template('netpan_control.html',user=current_user,files=files)

@views.route('/motify_file/<id>',methods=['POST','GET'])
@login_required
def motify_file(id):
    file=File.query.filter_by(id=id).first()
    if not file:
        flash('文件不存在！')
    elif file.owner!=current_user.id:
        flash('你无权修改他人的文件名！')
    else:
        if request.method=='POST':
            if os.path.isfile(os.path.join(UPLOAD_FOLDER,file.name)):
                os.rename(os.path.join(UPLOAD_FOLDER,file.name),os.path.join(UPLOAD_FOLDER,request.form.get('name')))
            file.name=request.form.get('name')
            db.session.commit()
            flash('文件名修改成功。')
            return redirect(url_for('views.netpan_control'))
    return render_template('motify_file.html',file=file,user=current_user)

@views.route('/delete_file/<id>')
@login_required
def delete_file(id):
    file=File.query.filter_by(id=id).first()
    if not file:
        flash('没有这个文件！')
    else:
        if file.owner!=current_user.id:
            flash('你没有权限删除其他人的文件！')
        else:
            if os.path.isfile(os.path.join(UPLOAD_FOLDER,file.name)):
                os.remove(os.path.join(UPLOAD_FOLDER,file.name))
            db.session.delete(file)
            db.session.commit()
            flash('删除成功。')
            return redirect(url_for('views.netpan_control'))

@views.route('/download_file/<id>')
@login_required
def download_file(id):
    file=File.query.filter_by(id=id).first()
    if not file:
        flash('没有这个文件！')
    else:
        if file.owner!=current_user.id:
            flash('你没有权限下载其他人的文件！')
        else:
            return send_file(os.path.join(UPLOAD_FOLDER,file.name))