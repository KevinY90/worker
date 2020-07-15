import os
import sys
import json
import time
from threading import Thread, Timer
from collections import deque
from server import connection


class Process:
    def __init__(
            self,
            task_handler,
            notifications_handler,
            available_tasks,
            db_queue,
            db_url
    ):
        self.task_handler = task_handler
        self.notifications_handler = notifications_handler
        self.available = available_tasks
        self.db = connection.DBConnection(db_url)
        self.db_update_queue = db_queue

    def do_tasks(self):
        while len(self.available):
            task = self.available.popleft()
            task.start()
        Timer(5, self.do_tasks).start()

    def perform_updates(self):
        queue = self.db_update_queue
        while len(self.db_update_queue):
            task_id, completed, task_queue, data, interval = queue.popleft()
            task = self.db.session.query(self.db.tasks).get(task_id)
            task.callCount += 1
            self.db.session.commit()
            if task.active:
                task_queue.zadd(
                    'idle',
                    {json.dumps(data): time.time()+int(interval)}
                )
        Timer(5, self.perform_updates).start()

    def run(self):
        Thread(
            target=self.task_handler.handle_task_queue
            ).start()
        Thread(
            target=self.notifications_handler.handle_notification_queue
            ).start()
        Thread(
            target=self.task_handler.enqueue_tasks, args=['idle']
            ).start()
        self.do_tasks()
        self.perform_updates()
