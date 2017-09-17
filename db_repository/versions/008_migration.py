from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_rooms = Table('dungeon_rooms', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('dungeon', INTEGER),
    Column('floor', INTEGER),
    Column('name', VARCHAR(length=120)),
    Column('neighbors', BLOB),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_rooms'].columns['neighbors'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_rooms'].columns['neighbors'].create()
