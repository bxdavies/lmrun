# coding: utf-8
from sqlalchemy import create_engine, Column, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, SMALLINT, TINYINT, BOOLEAN
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LocalAuthorityDistricts(Base):
    __tablename__ = 'local_authority_districts'

    id = Column(SMALLINT(5), primary_key=True)
    local_authority = Column(String(36), nullable=False)


class PropertyNames(Base):
    __tablename__ = 'property_names'

    id = Column(TINYINT(10), primary_key=True)
    name = Column(String(10), nullable=False)
    value = Column(SMALLINT(5), nullable=False)


class PropertyStatus(Base):
    __tablename__ = 'property_status'

    id = Column(TINYINT(4), primary_key=True)
    value = Column(String(11), nullable=False)


class Users(Base):
    __tablename__ = 'users'

    id = Column(BIGINT(10), primary_key=True)
    username = Column(String(32), nullable=False)
    creation_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    last_access_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    permitted_login = Column(TINYINT(1), nullable=False, server_default=text("1"))


class Locations(Base):
    __tablename__ = 'locations'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(100), nullable=False)
    author_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    local_authority_id = Column(ForeignKey('local_authority_districts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    difficulty = Column(TINYINT(4), nullable=False)
    description = Column(Text, nullable=False)

    author = relationship('Users')
    local_authority = relationship('LocalAuthorityDistricts')


class Guilds(Base):
    __tablename__ = 'guilds'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(100), nullable=False)
    date_added = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    teams = Column(INTEGER(11), nullable=False)
    location_id = Column(ForeignKey('locations.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    location = relationship('Locations')


class Properties(Base):
    __tablename__ = 'properties'
    __table_args__ = (
        Index('location', 'name'),
    )

    id = Column(BIGINT(20), primary_key=True)
    location_id = Column(ForeignKey('locations.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    property_id = Column(ForeignKey('property_names.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(Text, nullable=False)
    question = Column(LONGTEXT, nullable=False)
    answer = Column(LONGTEXT, nullable=False)

    location = relationship('Locations')
    property = relationship('PropertyNames')


class Games(Base):
    __tablename__ = 'games'

    id = Column(BIGINT(20), primary_key=True)
    guild_id = Column(ForeignKey('guilds.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    team = Column(Text(6), nullable=False)
    money = Column(SMALLINT(6), nullable=False, server_default=text("0"))
    current_property_id = Column(ForeignKey('properties.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    brown1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    brown2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    station1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    lightblue1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    lightblue2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    lightblue3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    pink1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    utility1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    pink2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    pink3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    station2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    orange1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    orange2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    orange3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    red1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    red2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    red3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    station3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    yellow1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    yellow2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    utility2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    yellow3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    green1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    green2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    green3 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    station4 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    darkblue1 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))
    darkblue2 = Column(ForeignKey('property_status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("1"))

    current_property = relationship('Properties')
    guild = relationship('Guilds')

    brown1_status = relationship('PropertyStatus', primaryjoin='Games.brown1 == PropertyStatus.id')
    brown2_status = relationship('PropertyStatus', primaryjoin='Games.brown2 == PropertyStatus.id')
    station1_status = relationship('PropertyStatus', primaryjoin='Games.station1 == PropertyStatus.id')
    lightblue1_status = relationship('PropertyStatus', primaryjoin='Games.lightblue1 == PropertyStatus.id')
    lightblue2_status = relationship('PropertyStatus', primaryjoin='Games.lightblue2 == PropertyStatus.id')
    lightblue3_status = relationship('PropertyStatus', primaryjoin='Games.lightblue3 == PropertyStatus.id')
    pink1_status = relationship('PropertyStatus', primaryjoin='Games.pink1 == PropertyStatus.id')
    utility1_status = relationship('PropertyStatus', primaryjoin='Games.utility1 == PropertyStatus.id')
    pink2_status = relationship('PropertyStatus', primaryjoin='Games.pink2 == PropertyStatus.id')
    pink3_status = relationship('PropertyStatus', primaryjoin='Games.pink3 == PropertyStatus.id')
    station2_status = relationship('PropertyStatus', primaryjoin='Games.station2 == PropertyStatus.id')
    orange1_status = relationship('PropertyStatus', primaryjoin='Games.orange1 == PropertyStatus.id')
    orange2_status = relationship('PropertyStatus', primaryjoin='Games.orange2 == PropertyStatus.id')
    orange3_status = relationship('PropertyStatus', primaryjoin='Games.orange3 == PropertyStatus.id')
    red1_status = relationship('PropertyStatus', primaryjoin='Games.red1 == PropertyStatus.id')
    red2_status = relationship('PropertyStatus', primaryjoin='Games.red2 == PropertyStatus.id')
    red3_status = relationship('PropertyStatus', primaryjoin='Games.red3 == PropertyStatus.id')
    station3_status = relationship('PropertyStatus', primaryjoin='Games.station3 == PropertyStatus.id')
    yellow1_status = relationship('PropertyStatus', primaryjoin='Games.yellow1 == PropertyStatus.id')
    yellow2_status = relationship('PropertyStatus', primaryjoin='Games.yellow2 == PropertyStatus.id')
    utility2_status = relationship('PropertyStatus', primaryjoin='Games.utility2 == PropertyStatus.id')
    yellow3_status = relationship('PropertyStatus', primaryjoin='Games.yellow3 == PropertyStatus.id')
    green1_status = relationship('PropertyStatus', primaryjoin='Games.green1 == PropertyStatus.id')
    green2_status = relationship('PropertyStatus', primaryjoin='Games.green2 == PropertyStatus.id')
    green3_status = relationship('PropertyStatus', primaryjoin='Games.green3 == PropertyStatus.id')
    station4_status = relationship('PropertyStatus', primaryjoin='Games.station4 == PropertyStatus.id')
    darkblue1_status = relationship('PropertyStatus', primaryjoin='Games.darkblue1 == PropertyStatus.id')
    darkblue2_status = relationship('PropertyStatus', primaryjoin='Games.darkblue2 == PropertyStatus.id')
