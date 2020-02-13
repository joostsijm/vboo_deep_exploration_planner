"""Jobs for scheduler module"""

from app import app, api


def sync_deep_exploration(region_id):
    """Check resources and refill if necessary"""
    app.sync_deep_exploration(region_id)

def schedule_orders():
    """Schedule deep exploration orders"""
    app.schedule_orders()

def start_deep_exploration_order(order_id):
    """Start deep exploration"""
    app.start_deep_exploration(order_id)
