from marshmallow import Schema, fields, ValidationError, pre_load
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import UserMixin

from app import db, login

@login.user_loader
def load_user(uuid):
    return User.query.get(int(uuid))

association_table = db.Table('association',
    db.Column('posts_id', db.Integer, db.ForeignKey('posts.uuid')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.uuid'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    is_current_user = db.Column(db.Boolean)

    def is_current_user(self):
        self.is_current_user = current_user.is_authenticated

    def get_id(self):
           return (self.uuid)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def __repr__(self):
        return '<User %r>' % self.username

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

# Schemas

class UserSchema(Schema):
    uuid = fields.Int(dump_only=True)
    username = fields.String()
    password_hash = fields.String()

class CategorySchema(Schema):
    uuid = fields.Int(dump_only=True)
    name = fields.String()
    colour = fields.String()

class PostSchema(Schema):
    uuid = fields.Int(dump_only=True)
    title = fields.String()
    body = fields.String()
    author = fields.Nested(UserSchema)
    categories = fields.Nested(CategorySchema, many=True)
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True, only=("title", "body", "author", "categories"))