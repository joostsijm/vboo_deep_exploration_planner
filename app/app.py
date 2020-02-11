"""General function module"""

import random
from datetime import datetime, timedelta

from telegram import ParseMode

from app import LOGGER, SCHEDULER, TELEGRAM_BOT, RESOURCE_NAMES, jobs, api, database


def check_deep_exploration(region_id):
    """Check resources and refill if necessary"""
    deep_explorations = api.download_deep_explorations(region_id)
    database.save_deep_explorations(region_id, deep_explorations)
    deep_exploration = database.get_active_deep_exploration(region_id)
    print(deep_exploration)
    return
    if do_refill and need_refill(regions, refill_percentage):
        max_seconds = max_refill_seconds(regions, refill_percentage, 900)
        random_seconds = random.randint(0, max_seconds)
        random_time_delta = timedelta(seconds=random_seconds)
        scheduled_date = datetime.now() + random_time_delta
        job_id = 'refill_{}_{}'.format(capital_id, resource_id)
        LOGGER.info(
            'Refil resource %s at %s (%s minutes)',
            resource_id,
            scheduled_date,
            round(random_time_delta.seconds / 60)
        )
        job = SCHEDULER.get_job(job_id)
        if not job:
            SCHEDULER.add_job(
                jobs.refill_resource,
                'date',
                args=[state_id, capital_id, resource_id, alt],
                id=job_id,
                run_date=scheduled_date
            )

def print_resources(regions):
    """print resources"""
    if regions:
        print('region                        expl max   D left    c %    t %')
        for region in regions.values():
            region['explored_percentage'] = 100 / region['maximum'] * region['explored']
            region['total_left'] = region['explored'] + region['limit_left']
            region['total_percentage'] = 100 / 2500 * region['total_left']
            print('{:25}: {:7.2f}{:4}{:4}{:5}{:7.2f}{:7.2f}'.format(
                region['region_name'],
                region['explored'],
                region['maximum'],
                region['deep_exploration'],
                region['limit_left'],
                region['explored_percentage'],
                region['total_percentage'],
            ))
    else:
        LOGGER.error('no region to print data')

def need_refill(regions, limit):
    """Check if refill is needed"""
    for region in regions.values():
        percentage = 100 / region['maximum'] * region['explored']
        if percentage < limit and region['limit_left']:
            return True
    return False

def max_refill_seconds(regions, limit, max_time):
    """Give random seconds for next refill"""
    lowest_percentage = limit
    for region in regions.values():
        percentage = 100 / region['maximum'] * region['explored']
        if percentage < lowest_percentage:
            lowest_percentage = percentage
    return int(max_time / limit * lowest_percentage)

def send_telegram_update(state_id, group_id, resource_name):
    """Send resource update to telegram"""
    resource_id = RESOURCE_NAMES[resource_name]
    # date = datetime.now()
    date = datetime.today().replace(hour=18, minute=5) - timedelta(1)
    print(date)
    message = database.get_work_percentage(state_id, resource_id, date, 1, 1)
    date = datetime.today().replace(hour=19, minute=5) - timedelta(1)
    print(date)
    message = database.get_work_percentage(state_id, resource_id, date, 1, 1)
    date = datetime.today().replace(hour=20, minute=5) - timedelta(1)
    print(date)
    message = database.get_work_percentage(state_id, resource_id, date, 1, 1)
    date = datetime.today().replace(hour=21, minute=5) - timedelta(1)
    print(date)
    message = database.get_work_percentage(state_id, resource_id, date, 1, 1)
    date = datetime.today().replace(hour=22, minute=5) - timedelta(1)
    print(date)
    message = database.get_work_percentage(state_id, resource_id, date, 1, 1)
    return
    if message:
        print(message)
        TELEGRAM_BOT.sendMessage(
            chat_id=group_id,
            text='```\n{}```'.format(message),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        LOGGER.error('no data for Telegram message')
