# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

basedir = os.path.abspath(os.path.dirname(__file__))

# App initialisation
app = Flask(__name__)
app.debug = True

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
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
    categories = db.relationship('Category', secondary=association_table, back_populates='category_id')

    def __repr__(self):
        return '<Post % r>' % self.title

class Category(db.Model):
    __tablename__ = 'category'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(50), nullable=True)
    category_id = db.relationship('Post', secondary=association_table, back_populates='categories')

    def __repr__(self):
        return '<Category %r>' % self.name

# Schema Objects

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

    def mutate(self, info, title, body, username, category):
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

# Routes
@app.route('/')
def index():
    return '<p>Hello World</p>'

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
