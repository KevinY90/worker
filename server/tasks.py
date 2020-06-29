import time
import sys
from threading import Thread, Timer
from http_api import Request


class TaskFactory:
    def __init__(self, connection, completed_job_queue, redis_conn):
        self.cursor = connection
        self.destination_queue = completed_job_queue
        self.redis_conn = redis_conn
    
    def create_task(self, task_data, connection):
        pass

    def run_on_task_end(self, destination):
        queue = self.redis_conn
        destination = self.destination_queue
        def send_to_notification_queue(*args, **kwargs):
            # add to notification queue 
            # get task data from args / kwargs
            # if send_notification is true in kwargs
            # send this task to notifications queue
        return send_to_notification_queue


class Task:
    def __init__(self, task_data, run_when_complete):
        self.task_data = task_data
        self.is_notification_required = run_when_complete
    
    def __del__(self):
        self.is_notification_required(self.task_data)
    

class PollApi(Task):
    def __init__(self, task_data, cache_conn, req, parse_fn):
        super().__init__(task_data)
        self.req = req
        self.parse = parse_fn
        self.store = cache_conn

    def analyze_response(self):
        res = self.req.make_get_request()
        self.task_data.notify = self.parse(res)

    def cache_results(self):
        # write to redis cache 

