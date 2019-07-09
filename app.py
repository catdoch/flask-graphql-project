# Imports
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_graphql import GraphQLView

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

from models import User, Category, Post
from schemas import schema

# Routes
@app.route('/')
def index():
    return render_template('home.html')

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

@app.route('/add-post')
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
        return 'Post added, post id={}'.format(post.uuid)
    except Exception as e:
        return(str(e))

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

@app.route('/getall')
def get_all():
    try:
        users=User.query.all()
        return jsonify([e.serialize() for e in users])
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

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
