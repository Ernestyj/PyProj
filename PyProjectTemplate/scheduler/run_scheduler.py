# -*- coding: utf-8 -*-
import os

from reaper.reaper_scheduler import ActionScheduler


# PROJECT_RUNTIME_STAGE = os.environ['PROJECT_RUNTIME_STAGE']
PROJECT_RUNTIME_STAGE = 'feature'


if __name__ == "__main__":
    app = ActionScheduler()
    try:
        app.start()
    except (KeyboardInterrupt, SystemExit):
        app.shutdown()