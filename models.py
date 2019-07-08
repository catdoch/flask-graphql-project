# Imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from app import db

# Models
association_table = db.Table('association',
    db.Column('posts_id', db.Integer, db.ForeignKey('posts.uuid')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.uuid'))
)

class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'username': self.username,
            'uuid': self.uuid
        }

class Post(db.Model):
    __tablename__ = 'posts'

    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    categories = db.relationship('Category', secondary=association_table, back_populates='category_id', lazy='dynamic')

    def __repr__(self):
        return '<Post % r>' % self.title

class Category(db.Model):
    __tablename__ = 'category'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(50), nullable=True)
    category_id = db.relationship('Post', secondary=association_table, back_populates='categories', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name

    def serialize(self):
        return {
            'name': self.name,
            'colour': self.colour
        }
