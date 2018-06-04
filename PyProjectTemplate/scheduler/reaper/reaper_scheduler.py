# -*- coding: utf-8 -*-
import traceback
from pymongo import MongoClient
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_ALL_JOBS_REMOVED, EVENT_JOB_EXECUTED, EVENT_ALL
from requests.exceptions import RequestException
from pymongo.errors import PyMongoError

from reaper.settings import *
from reaper.utility import *
from reaper.utility import get_cur_time


# apscheduler settings
APSCHEDULER_SETTINGS = {
    'jobstores': {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite'),
        # 'mongo': MongoDBJobStore(client=mongo_client, database=mongo_alert['db'], collection=mongo_alert['job_collection']),
    },
    'executors': {
        'default': ThreadPoolExecutor(30),
        'processpool': ProcessPoolExecutor(4)
    },
    'job_defaults': {
        'coalesce': True,
        'max_instances': 3
    }
}


# job time define
REAP_INTERVAL_SECONDS = 1 * 60
GATHER_FAILED_TASKS_INTERVAL_SECONDS = 1 * 60
DEFAULT_MISFIRE_GRACE_TIME = 60 * 60  # the time (in seconds) how much this job’s execution is allowed to be late


# get mongo
# mongo_task = PROJECT_CONFIG['mongo_alert_reaper']
# timestamp_collection = MongoClient(mongo_task['host'], mongo_task['port'])[mongo_task['db']][mongo_task['timestamp_collection']]
# COL_REAPER_BEGIN = "reaper_begin"
# COL_CHECKER_BEGIN = "checker_begin"


class ActionScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler(jobstores=APSCHEDULER_SETTINGS['jobstores'],
                                           executors=APSCHEDULER_SETTINGS['executors'],
                                           job_defaults=APSCHEDULER_SETTINGS['job_defaults'],
                                           timezone=TIMEZONE_PST8PDT)
        pass

    def start(self):
        self._add_event_listener()
        # self._add_example_jobs()
        self._add_jobs()
        self.scheduler.start()

    def shutdown(self):
        # self.scheduler.remove_all_jobs()  # save all jobs into sqlite, do not remove them
        self.scheduler.shutdown()

    def _add_event_listener(self):
        self.scheduler.add_listener(ActionScheduler.listener_jobs_status, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.scheduler.add_listener(ActionScheduler.listener_all_jobs_finished, EVENT_ALL_JOBS_REMOVED)

    # examples
    def _add_example_jobs(self):
        import datetime
        self.scheduler.add_job(func=ActionScheduler.job_example, args=["cron", ], trigger='cron', second='*/5',
                               misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, id="cron")
        self.scheduler.add_job(func=ActionScheduler.job_example, args=["interval", ], trigger='interval', seconds=60,
                               misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, id="interval")
        self.scheduler.add_job(func=ActionScheduler.job_example, args=["date", ], trigger='date',
                               run_date=get_cur_time()+datetime.timedelta(seconds=12), id="date")

    # examples
    @staticmethod
    def job_example(job_type):
        print("job_example: {}".format(job_type))

    def _add_jobs(self):
        # add reap alerts immediate job TODO test
        # self.scheduler.add_job(id="reap_alerts_immediate", func=ActionScheduler.job_reap_alerts_and_start_action_tasks, args=[],
        #                        misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, )
        # add reap alerts interval job
        # self.scheduler.add_job(id="reap_alerts", func=ActionScheduler.job_reap_alerts_and_start_action_tasks,
        #                        args=[], trigger='interval', seconds=REAP_INTERVAL_SECONDS,
        #                        misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, )
        # add gather & retry failed action tasks immediate job TODO test
        # self.scheduler.add_job(id="check_tasks_immediate", func=ActionScheduler.job_gather_and_retry_failed_action_tasks, args=[],
        #                        misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, )
        # add gather & retry failed action tasks interval job
        # self.scheduler.add_job(id="check_tasks", func=ActionScheduler.job_gather_and_retry_failed_action_tasks,
        #                        args=[], trigger='interval', seconds=GATHER_FAILED_TASKS_INTERVAL_SECONDS,
        #                        misfire_grace_time=DEFAULT_MISFIRE_GRACE_TIME, replace_existing=True, )
        pass

    @staticmethod
    def listener_all_jobs_finished(event):  # this would hardly be invoked
        logger_.info('All jobs are done.')

    @staticmethod
    def listener_jobs_status(event):
        if event.exception:
            logger_.warn('Job {} crashed.'.format(event.job_id))
        else:
            logger_.info('Job {} executed.'.format(event.job_id))