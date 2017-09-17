from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_floors = Table('dungeon_floors', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('room', INTEGER),
    Column('details', VARCHAR(length=256)),
    Column('options', VARCHAR),
)

dungeon_events = Table('dungeon_events', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('room', Integer),
    Column('details', String(length=256)),
    Column('options', String),
)

dungeon_rooms = Table('dungeon_rooms', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('dungeon', Integer),
    Column('floor', Integer),
    Column('neighbors', PickleType),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_floors'].drop()
    post_meta.tables['dungeon_events'].create()
    post_meta.tables['dungeon_rooms'].columns['neighbors'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_floors'].create()
    post_meta.tables['dungeon_events'].drop()
    post_meta.tables['dungeon_rooms'].columns['neighbors'].drop()
