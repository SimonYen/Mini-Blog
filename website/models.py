from . import db
from flask_login import UserMixin
from datetime import datetime
from pytz import timezone

def shanghai_time():
    now_utc=datetime.now(timezone('UTC'))
    now_shanghai=now_utc.astimezone(timezone('Asia/Shanghai'))
    return now_shanghai.strftime('%Y年%m月%d日 %H:%M')



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(100), unique=True)
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    created_time = db.Column(db.String(200),default=shanghai_time)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    author_name=db.Column(db.String(300))
    article = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    created_time = db.Column(db.String(200),default=shanghai_time)

