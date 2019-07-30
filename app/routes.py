# Imports
from flask import request, jsonify, render_template

from app import db, app
from app.models import User, Category, Post, posts_schema, users_schema, categories_schema

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