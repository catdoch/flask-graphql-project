"""empty message

Revision ID: 1f5f70390f22
Revises: 1e2c8d0b8345
Create Date: 2019-07-30 09:31:34.123346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f5f70390f22'
down_revision = '1e2c8d0b8345'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64)))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.INTEGER(), server_default=sa.text("nextval('users_uuid_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('association',
    sa.Column('posts_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.uuid'], name='association_category_id_fkey'),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.uuid'], name='association_posts_id_fkey')
    )
    op.create_table('category',
    sa.Column('uuid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('colour', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='category_pkey')
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