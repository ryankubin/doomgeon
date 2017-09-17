from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_event = Table('dungeon_event', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('room', INTEGER),
    Column('details', VARCHAR(length=256)),
    Column('map', INTEGER),
    Column('type', VARCHAR(length=256)),
)

dungeon_event = Table('dungeon_event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('room_id', Integer),
    Column('map_id', Integer),
    Column('type', String(length=256)),
    Column('details', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_event'].columns['map'].drop()
    pre_meta.tables['dungeon_event'].columns['room'].drop()
    post_meta.tables['dungeon_event'].columns['map_id'].create()
    post_meta.tables['dungeon_event'].columns['room_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_event'].columns['map'].create()
    pre_meta.tables['dungeon_event'].columns['room'].create()
    post_meta.tables['dungeon_event'].columns['map_id'].drop()
    post_meta.tables['dungeon_event'].columns['room_id'].drop()
