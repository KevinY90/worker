import time
import sys
import json
import pickle
from threading import Thread, Timer
from .request_generator import Request
from .functions import create_parser


class TaskCreator:
    def __init__(self, container, queue, db_queue):
        self.container = container
        self.queue = queue
        self.mem = {}
        self.db_queue = db_queue

    def create_task(self, task_data):
        task_data = json.loads(task_data)
        parse_fn = None
        url_data = task_data['url_obj']
        if url_data.get('fields'):
            targeted_fields = url_data['fields']
            if self.mem.get(targeted_fields):
                parse_fn = self.mem[targeted_fields]
            else:
                parse_fn = create_parser(targeted_fields)
                self.mem[targeted_fields] = parse_fn
        req = Request(
            url_data['url'],
            url_data['params'],
            url_data['headers'],
            )
        rwc = self.run_when_complete()
        self.container.append(PollEndpoint(task_data, req, parse_fn, rwc))

    def run_when_complete(self):
        task_queue = self.queue
        db_queue = self.db_queue

        def process_completed_task(task_data):
            should_notify = task_data.get('notify')
            interval = task_data['task_obj']['interval']
            complete = task_data['task_obj']['completed']
            if should_notify:
                notification = pickle.dumps({
                    'user': task_data['user_obj']['email'],
                    'data': task_data['notify'],
                    'type': task_data['task_obj']['notification_type'],
                    'task_message':
                        task_data['task_obj']['notification_message'],
                })
                task_queue.rpush('notifications', notification)
            if not complete and task_data.get('notify'):
                del task_data['notify']
            db_queue.append(
                (
                    task_data['task_obj']['id'],
                    should_notify,
                    task_queue,
                    task_data,
                    interval
                )
            )
        return process_completed_task


class Task:
    def __init__(self, task_data, run_when_complete):
        self.task_data = task_data
        self.process_completed_task = run_when_complete

    def __del__(self):
        self.process_completed_task(self.task_data)


class PollEndpoint(Task):
    def __init__(self, task_data, req, parse_fn, on_complete):
        super().__init__(task_data, on_complete)
        self.req = req
        self.parse = parse_fn

    def analyze_response(self, response):
        if response.status_code == 200 or response.status_code == 201:
            response = json.loads(response.text)
            notifications = self.parse(response)
            self.task_data['notify'] = notifications if notifications else None

    def start(self):
        response = self.req.make_get_request()
        self.analyze_response(response)
