from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
    Column('about_me', String),
    Column('last_seen', DateTime),
    Column('first', String),
    Column('last', String),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('about_me', String(length=140)),
    Column('firstname', String(length=40)),
    Column('lastname', String(length=40)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['first'].drop()
    pre_meta.tables['user'].columns['last'].drop()
    post_meta.tables['user'].columns['firstname'].create()
    post_meta.tables['user'].columns['lastname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['first'].create()
    pre_meta.tables['user'].columns['last'].create()
    post_meta.tables['user'].columns['firstname'].drop()
    post_meta.tables['user'].columns['lastname'].drop()
