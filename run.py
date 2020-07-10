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

    env = {}
    if os.environ.get('REMOTE'):
        env['database'] = {
            'url': os.environ['DATABASE_URL']
        }
        env['redis'] = {
            'host': os.environ['redis_host'],
            'port': int(os.environ['redis_port']),
            'password': os.environ['redis_passwd'],
            'db': int(os.environ['redis_db']),
            'expire': int(os.environ['redis_expire']),
        }
        env['email'] = {
            'worker_email': os.environ['worker_email'],
            'password': os.environ['worker_passwd'],
            'smtp_server': os.environ['smtp_server'],
            'port': int(os.environ['smtp_port']),
        }
        env['task_queues'] = [os.environ['task_queues']]
        env['notification_queues'] = [os.environ['notification_queues']]
        print(env)
    else:
        env = config
    
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
