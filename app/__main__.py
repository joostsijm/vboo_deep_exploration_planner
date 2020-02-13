"""Main app"""

import time
import sys

from app import SCHEDULER, LOGGER, RESOURCE_NAMES, jobs


if __name__ == '__main__':
    jobs.schedule_orders()
    # jobs.sync_deep_exploration(4002)
    # jobs.start_deep_exploration_order(2)
    sys.exit()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()
