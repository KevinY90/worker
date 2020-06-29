import time
from threading import Thread, Timer


class TaskHandler:
    def __init__(self, subscription, db_conn, task_dir, task_factory):
        self.channel = subscription
        self.task_dir = task_dir
        self.factory = task_factory

    def gather_tasks(self):
        while True:
            tasks = self.channel.listen()
            for instruction in tasks:
                new_task = self.factory.create_task(instruction)

class NotificationHandler:
    def __init__(self, job_queue, email_generator, sms_generator=None):
        self.job_queue = job_queue
        self.email_generator = email_generator
        self.sms_generator = sms_generator
    
    def process_notifications(self):
        # grab items from notifications queue
        pass

