import time
import json
import pickle
from threading import Timer


class Handler:
    def __init__(self, names, queue):
        self.names = names
        self.queue = queue
    
    def process_queue(self, handler):
        queue = self.queue
        def get_from_queue():
            for job_queue in self.names:
                job = self.queue.lpop(job_queue)
                if job:
                    handler(job)
            Timer(3, get_from_queue).start()
        return get_from_queue


class TaskHandler(Handler):
    def __init__(self, job_queues, queue, task_factory):
        super().__init__(job_queues, queue)
        self.factory = task_factory
        self.get_tasks = self.process_queue(self.factory.create_task)
    
    def handle_task_queue(self):
        self.get_tasks()

    def enqueue_tasks(self, key):
        def get_next():
            return self.queue.zrange(key, 0, 0, withscores=True)
        from_set = get_next()
        if from_set:
            next_task, interval = from_set.pop()
            while time.time() > interval:
                self.queue.rpush('tasks', next_task)
                self.queue.zpopmin(key, 1)
                from_set = get_next()
                if from_set:
                    next_task, interval = from_set.pop()
                else:
                    break
        Timer(15, self.enqueue_tasks, args=[key]).start()


class NotificationHandler(Handler):
    def __init__(self, job_queues, queue, email_generator, sms_generator=None):
        super().__init__(job_queues, queue)
        self.email_generator = email_generator
        self.sms_generator = sms_generator
        self.get_notifications = self.process_queue(self.send_notification)
    
    def send_notification(self, data):
        notification = pickle.loads(data)
        if notification['type'] == 'email':
            message = self.compose_message(notification['data'], notification['task_message'])
            self.email_generator.send_email(message, notification['user'])

    def compose_message(self, data, task_msg):
        message = ['{} {} {}'.format(t,e,v) for t,e,v in data]
        message.append(task_msg)
        return '\n'.join(message)

    def handle_notification_queue(self):
        self.get_notifications()


