from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_events = Table('dungeon_events', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('room', INTEGER),
    Column('details', VARCHAR(length=256)),
    Column('options', VARCHAR),
)

dungeon_maps = Table('dungeon_maps', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('player', VARCHAR(length=64)),
)

dungeon_rooms = Table('dungeon_rooms', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('dungeon', INTEGER),
    Column('floor', INTEGER),
    Column('name', VARCHAR(length=120)),
    Column('neighbors', VARCHAR(length=256)),
)

players = Table('players', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('currentRoom', VARCHAR(length=120)),
)

dungeon_event = Table('dungeon_event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('room', Integer),
    Column('details', String(length=256)),
    Column('options', String),
)

dungeon_map = Table('dungeon_map', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('player', String(length=64)),
)

dungeon_room = Table('dungeon_room', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('dungeon', Integer),
    Column('floor', Integer),
    Column('neighbors', String(length=256)),
)

player = Table('player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('currentRoom', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_events'].drop()
    pre_meta.tables['dungeon_maps'].drop()
    pre_meta.tables['dungeon_rooms'].drop()
    pre_meta.tables['players'].drop()
    post_meta.tables['dungeon_event'].create()
    post_meta.tables['dungeon_map'].create()
    post_meta.tables['dungeon_room'].create()
    post_meta.tables['player'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_events'].create()
    pre_meta.tables['dungeon_maps'].create()
    pre_meta.tables['dungeon_rooms'].create()
    pre_meta.tables['players'].create()
    post_meta.tables['dungeon_event'].drop()
    post_meta.tables['dungeon_map'].drop()
    post_meta.tables['dungeon_room'].drop()
    post_meta.tables['player'].drop()
