"""Main application"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import joinedload

from app import SESSION, RESOURCE_MAX
from app.models import Region, DeepExploration


def save_deep_explorations(region_id, deep_explorations):
    """Save resources to database"""
    session = SESSION()
    for deep_exploration_id, deep_exploration_dict in deep_explorations.items():
        deep_exploration = session.query(DeepExploration).get(deep_exploration_id)
        if deep_exploration:
            break
        deep_exploration = DeepExploration()
        deep_exploration.id = deep_exploration_id
        region = session.query(Region).get(region_id)
        if not region:
            region = save_region(session, region_id)
        deep_exploration.region_id = region_id
        deep_exploration.resource_type = deep_exploration_dict['resource_type']
        deep_exploration.until_date_time = deep_exploration_dict['until_date_time']
        session.add(deep_exploration)
    session.commit()
    session.close()

def get_active_deep_exploration(region_id):
    """Get active deep exploration in a region"""
    session = SESSION()
    deep_exploration = session.query(DeepExploration) \
        .filter(DeepExploration.region_id == region_id) \
        .filter(DeepExploration.until_date_time >= datetime.now()) \
        .first()
    session.close()
    return deep_exploration


def save_region(session, region_id):
    """Save player to database"""
    region = Region()
    region.id = region_id
    region.name = 'UNKNOWN'
    session.add(region)
    return region
