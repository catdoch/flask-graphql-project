# Imports
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from marshmallow import Schema, fields, ValidationError, pre_load

basedir = os.path.abspath(os.path.dirname(__file__))

# App initialisation
app = Flask(__name__)
app.debug = True

# Configs
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

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

# Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/viewall/posts')
def post_index():
    return render_template('posts.html')

@app.route('/add-post-form')
def post_form_index():
    return render_template('add-post-form.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    username = request.args.get('username')
    try:
        user=User(username=username)
        db.session.add(user)
        db.session.commit()
        return jsonify(value='success')
    except Exception as e:
        if 'UniqueViolation' in str(e):
            return jsonify(value='Username already exists, please choose another')
        else:
            return jsonify(value=str(e))

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    categories = []
    title = request.args.get('title')
    body = request.args.get('body')
    author = User.query.filter_by(username=request.args.get('author')).first()
    categorySplit = request.args.get('categories').split(',')
    for cats in categorySplit:
        categories.append(Category.query.filter_by(name=cats).first())
    try:
        post = Post(
            title=title,
            body=body,
            author=author,
            categories=categories
        )
        db.session.add(post)
        db.session.commit()
        return jsonify(value='success')
    except Exception as e:
        return(str(e))
    return render_template('add-post-form.html')

@app.route('/add-category')
def add_category():
    name = request.args.get('name')
    colour = request.args.get('colour')
    try:
        category = Category(
            name=name,
            colour=colour
        )
        db.session.add(category)
        db.session.commit()
        return 'Category added, category name={}'.format(category.name)
    except Exception as e:
        return(str(e))

@app.route('/getall/posts')
def get_all_posts():
    try:
        posts=Post.query.all()
        result = posts_schema.dump(posts)
        return jsonify(result)
    except Exception as e:
        return(str(e))

@app.route('/getall/users')
def get_all_users():
    try:
        users=User.query.all()
        result = users_schema.dump(users)
        return jsonify(result)
    except Exception as e:
        return(str(e))

@app.route('/getall/categories')
def get_all_categories():
    try:
        categories=Category.query.all()
        result = categories_schema.dump(categories)
        return jsonify(result)
    except Exception as e:
        return(str(e))

@app.route('/add/form', methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        username=request.form.get('name')
        try:
            user=User(username=username)
            db.session.add(user)
            db.session.commit()
            return 'User added'
        except Exception as e:
            return(str(e))

    return render_template('form.html')

class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )

class CategoryObject(SQLAlchemyObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    all_categories = SQLAlchemyConnectionField(CategoryObject)

schema = graphene.Schema(query=Query)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)
        category = graphene.String(required=True)

    post = graphene.Field(lambda: PostObject)

    def mutate(self, info, title, body, username, category, name):
        user = User.query.filter_by(username=username).first()
        category = Category.query.filter_by(name=name).first()
        post = Post(title=title, body=body, category=category)

        if user is not None:
            post.author = user

        db.session.add(post)
        db.session.commit()

        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
