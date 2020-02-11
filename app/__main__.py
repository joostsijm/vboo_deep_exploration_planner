"""Main app"""

import time
import sys

from app import SCHEDULER, LOGGER, RESOURCE_NAMES, jobs


if __name__ == '__main__':
    jobs.check_deep_exploration(4002)
    sys.exit()

    add_telegram_update_job(2788, '@vn_resources', 'gold')
    add_telegram_update_job(2788, '@vn_uranium_resources', 'uranium')

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()

def add_telegram_update_job(state_id, telegram_id, resource_type):
    """Add telegram update job"""
    SCHEDULER.add_job(
        jobs.send_telegram_update,
        'cron',
        args=[state_id, telegram_id, resource_type],
        id='{}_send_telegram_update_{}'.format(state_id, resource_type),
        replace_existing=True,
        minute='5'
    )
