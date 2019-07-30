"""empty message

Revision ID: 21189bcc6f6d
Revises: 
Create Date: 2019-07-30 09:17:42.577901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21189bcc6f6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64)))
    # op.drop_table('association')
    # op.drop_table('category')
    # op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.INTEGER(), server_default=sa.text("nextval('users_uuid_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('category',
    sa.Column('uuid', sa.INTEGER(), server_default=sa.text("nextval('category_uuid_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('colour', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='category_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('association',
    sa.Column('posts_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.uuid'], name='association_category_id_fkey'),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.uuid'], name='association_posts_id_fkey')
    )
    op.create_table('posts',
    sa.Column('uuid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.uuid'], name='posts_author_id_fkey'),
    sa.PrimaryKeyConstraint('uuid', name='posts_pkey')
    )
    # ### end Alembic commands ###