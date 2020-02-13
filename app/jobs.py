"""Jobs for scheduler module"""

from app import app, api


def sync_deep_exploration(region_id):
    """Check resources and refill if necessary"""
    app.sync_deep_exploration(region_id)

def start_orders():
    """Start deep exploration orders"""
    app.start_orders()

def start_deep_exploration(order_id):
    """Start deep exploration"""
    app.start_deep_exploration(order_id)
