"""General function module"""

import random
from datetime import datetime, timedelta

from app import LOGGER, SCHEDULER, RESOURCE_IDS, DEEP_EXPLORATION_MAX , jobs, api, database


def sync_deep_exploration(region_id):
    """Check resources and refill if necessary"""
    deep_explorations = api.download_deep_explorations(region_id)
    database.save_deep_explorations(region_id, deep_explorations)

def start_orders():
    """start deep exploration orders"""
    orders = database.get_orders()
    for order in orders:
        deep_exploration = database.get_active_deep_exploration(order.region_id)
        if deep_exploration is None:
            sync_deep_exploration(order.region_id)
        deep_exploration = database.get_active_deep_exploration(order.region_id)
        start_date = deep_exploration.until_date_time if deep_exploration else datetime.now()
        max_seconds = 300
        random_seconds = random.randint(0, max_seconds)
        scheduled_date = start_date + timedelta(seconds=random_seconds)
        LOGGER.info(
            'Deep exploration at %s for %s in %s',
            scheduled_date.strftime("%Y-%m-%d %H:%M"),
            RESOURCE_IDS[order.resource_type],
            order.region_id
        )
        SCHEDULER.add_job(
            jobs.start_deep_exploration,
            'date',
            args=[order.id],
            id='deep_exploration_{}_{}'.format(order.region_id, order.resource_type),
            replace_existing=True,
            run_date=scheduled_date
        )

def start_deep_exploration(order_id):
    """Start deep exploration"""
    LOGGER.info('Start order %s', order_id)
    order = database.get_order(order_id)
    order_types = {
        0: get_max_points, # max
        1: get_fixed_points, # fixed
        2: get_percentage_points, # percentage
        3: get_auto_points, # auto
    }
    if order.order_type in order_types:
        points = order_types[order.order_type](order)
        print(points)
        state = database.get_state(order.region_id)
        api.deep_explorate(
            state.id, order.region_id, order.resource_type, points, False
        )


def get_max_points(order):
    """Get  deep exploration points for order"""
    region = database.get_region(order.region_id)
    resource_limit = region.get_limit(order.resource_type)
    return DEEP_EXPLORATION_MAX[order.resource_type] - resource_limit

def get_fixed_points(order):
    """Get  deep exploration points for order"""
    return order.amount
    
def get_percentage_points(order):
    """Get  deep exploration points for order"""
    return 1
    
def get_auto_points(order):
    """Get  deep exploration points for order"""
    return 1
