import os
import sys
from threading import Thread


class Process:
    def __init__(self, task_handler, task_map):
        self.task_handler = task_handler

    def start_process(self):
        Thread(target=self.task_handler.gather_tasks).start()
