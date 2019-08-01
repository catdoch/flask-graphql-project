# Imports
from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_graphql import GraphQLView
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import User, Category, Post, posts_schema, users_schema, categories_schema
from app.graphql.schemas import schema
from app.forms import LoginForm, RegistrationForm


# Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/viewall/posts')
@login_required
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
    userId = current_user.get_id()
    title = request.args.get('title')
    body = request.args.get('body')
    author = User.query.filter_by(uuid=userId).first()
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

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
