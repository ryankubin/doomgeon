from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_room = Table('dungeon_room', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=120)),
    Column('dungeon', INTEGER),
    Column('floor', INTEGER),
    Column('neighbors', VARCHAR(length=256)),
)

dungeon_room = Table('dungeon_room', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('dungeon_id', Integer),
    Column('floor', Integer),
    Column('neighbors', String(length=256), default=ColumnDefault('')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_room'].columns['dungeon'].drop()
    post_meta.tables['dungeon_room'].columns['dungeon_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_room'].columns['dungeon'].create()
    post_meta.tables['dungeon_room'].columns['dungeon_id'].drop()
