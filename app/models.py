"""Database models"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class State(Base):
    """Model for state"""
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Region(Base):
    """Model for region"""
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gold_limit = Column(SmallInteger)
    oil_limit = Column(SmallInteger)
    ore_limit = Column(SmallInteger)
    uranium_limit = Column(SmallInteger)
    diamond_limit = Column(SmallInteger)

    def get_limit(self, resource_type):
        """get limit for resoruce type"""
        limit = {
            0: self.gold_limit,
            3: self.oil_limit,
            4: self.ore_limit,
            11: self.uranium_limit,
            15: self.diamond_limit,
        }
        return limit[resource_type] if resource_type in limit else None


class StateRegion(Base):
    """Model for state region"""
    __tablename__ = 'state_region'
    state_id = Column(Integer, ForeignKey('state.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('region.id'), primary_key=True)
    from_date_time = Column(DateTime, primary_key=True)
    until_date_time = Column(DateTime)

    region = relationship(
        'Region',
        backref=backref('state_regions', lazy='dynamic')
    )
    state = relationship(
        'State',
        backref=backref('state_regions', lazy='dynamic')
    )


class DeepExploration(Base):
    """Model for deep exploration"""
    __tablename__ = 'deep_exploration'
    id = Column(Integer, primary_key=True)
    until_date_time = Column(DateTime)
    points = Column(Integer)
    resource_type = Column(SmallInteger)
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(
        'Region',
        backref=backref('deep_explorations', lazy='dynamic')
    )


class DeepExplorationOrder(Base):
    """Model for deep exploration order"""
    __tablename__ = 'deep_exploration_order'
    id = Column(Integer, primary_key=True)
    resource_type = Column(SmallInteger, nullable=False)
    order_type = Column(SmallInteger, nullable=False)
    amount = Column(Integer)
    from_date_time = Column(DateTime)
    until_date_time = Column(DateTime)

    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(
        'Region',
        backref=backref('resource_stats', lazy='dynamic')
    )

    order_types = {
        0: 'max',
        1: 'fixed',
        2: 'percentage',
        3: 'auto',
    }

    def order_type_name(self):
        """Type name"""
        if self.order_type in self.order_types:
            return self.order_types[self.type]
        return 'unknown'
