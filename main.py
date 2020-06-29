import yaml
import argparse
from server import connection
# from server.tasks import TaskFactory
# from server.email import EmailGenerator
# from server.handler import TaskHandler, NotificationHandler
# from server.process import Process



def main(opt):
    with open(opt['config']) as config_file:
        config = yaml.safe_load(config_file)
    for k,v in config.items():
        print(k , v)
    
    redis = connection.Redis(config['redis'])
    pubsub = redis.publish_subscribe()
    pubsub.subscribe(config['channel'])
    print(redis.check_health())
    db_connection = connection.DBConnection(config['database'])
    print(db_connection)
    task_map = {}

    # notification_handler = NotificationHandler(
    #     redis, 
    #     EmailGenerator(config['email'])
    # )

    # task_handler = TaskHandler(
    #     pubsub, 
    #     task_map,
    #     TaskFactory(db_connection),
    # )
    
    # process = Process(task_handler, task_map)


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument(
        "-c",
        "--config",
        default='defaults.yml',
        type=str,
    )
    main(vars(arguments.parse_args()))
