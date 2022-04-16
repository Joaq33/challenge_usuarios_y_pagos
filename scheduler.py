import datetime
import sys
import os
import logging.config

from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient
from decouple import config

from gen_payments import gen_payments, logger

# Set file logger
logger = logging.getLogger("scheduler")


def task_payments():
    """
    This function is called by the scheduler every 30 days
    :return:
    """
    logger.info("Generando pagos")
    gen_payments()


def run_scheduler():
    """
    The scheduler framework is created here
    :return:
    """
    # Set up the scheduler
    scheduler = BlockingScheduler()

    # If run with '--clear' argument, clear the pending jobs in the database
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        scheduler.remove_all_jobs()

    # Connect to DB and retrieve pending jobs
    store = MongoDBJobStore(client=MongoClient(config('MONGO_URI')))
    saved_jobs = store.get_all_jobs()
    job_stores = {
        'mongo': store
    }

    # configure the scheduler to use the job store
    scheduler.configure(jobstores=job_stores)

    # Add the job to the scheduler, if it doesn't exist, trigger it now
    scheduler.add_job(task_payments,
                      'interval',
                      days=30,
                      id="nuevo",
                      replace_existing=True,
                      jobstore='mongo',
                      next_run_time=saved_jobs[0].next_run_time if len(
                          saved_jobs) > 0 else datetime.datetime.now()
                      )

    # Start the scheduler
    try:
        scheduler.start()
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    logger.info("Run with --clear parameter to remove existing jobs")
    logger.info("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))
    run_scheduler()
