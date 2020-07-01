import os
import yaml
import argparse
from collections import deque
from server import connection
from server.email import EmailGenerator
from server.handler import TaskHandler, NotificationHandler
from server.process import Process
from server.tasks import TaskCreator


def main(opt):
    
    with open(opt['config']) as config_file:
        config = yaml.safe_load(config_file)
    env = {k:v for k, v in config.items()} if os.environ.get('production') else config
 
    
    redis_conn = connection.Redis(env['redis'])
    db_queue = deque()
    tasks_container = deque()
    notification_handler = NotificationHandler(
        env['notification_queues'],
        redis_conn.connection, 
        EmailGenerator(env['email'])
    )

    task_handler = TaskHandler(
        env['task_queues'],
        redis_conn.connection,
        TaskCreator(
            tasks_container,
            redis_conn.connection, 
            db_queue,
        ),
    )
    process = Process(
        task_handler,
        notification_handler,
        tasks_container,
        db_queue,
        env['database'],
        )
    process.run()


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument(
        "-c",
        "--config",
        default='defaults.yml',
        type=str,
    )
    main(vars(arguments.parse_args()))
