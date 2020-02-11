"""Jobs for scheduler module"""

from app import app, api


def check_deep_exploration(region_id):
    """Check resources and refill if necessary"""
    app.check_deep_exploration(region_id)
