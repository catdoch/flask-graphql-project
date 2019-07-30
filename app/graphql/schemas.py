import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app import app, db
from app.models import Post, User, Category

class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post

class PostConnection(graphene.relay.Connection):
    class Meta:
        node = PostObject

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User

class UserConnection(graphene.relay.Connection):
    class Meta:
        node = UserObject

class CategoryObject(SQLAlchemyObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostConnection)
    all_users = SQLAlchemyConnectionField(UserConnection)
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
