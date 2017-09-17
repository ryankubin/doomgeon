from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_floors = Table('dungeon_floors', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('room', Integer),
    Column('details', String(length=256)),
)

dungeon_maps = Table('dungeon_maps', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('player', String(length=64)),
)

dungeon_rooms = Table('dungeon_rooms', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('dungeon', Integer),
    Column('floor', Integer),
)

players = Table('players', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('currentRoom', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dungeon_floors'].create()
    post_meta.tables['dungeon_maps'].create()
    post_meta.tables['dungeon_rooms'].create()
    post_meta.tables['players'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dungeon_floors'].drop()
    post_meta.tables['dungeon_maps'].drop()
    post_meta.tables['dungeon_rooms'].drop()
    post_meta.tables['players'].drop()
