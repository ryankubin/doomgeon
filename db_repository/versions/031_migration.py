from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dungeon_map = Table('dungeon_map', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('player', INTEGER),
    Column('rooms', VARCHAR),
    Column('floor', INTEGER),
)

dungeon_map = Table('dungeon_map', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('player_id', Integer),
    Column('rooms', String, default=ColumnDefault('{}')),
    Column('floor', Integer, default=ColumnDefault(1)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_map'].columns['player'].drop()
    post_meta.tables['dungeon_map'].columns['player_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dungeon_map'].columns['player'].create()
    post_meta.tables['dungeon_map'].columns['player_id'].drop()
