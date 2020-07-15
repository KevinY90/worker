import redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, mapper
from collections import defaultdict


class Redis:
    def __init__(self, options):
        self.connection = self.create_connection(options)

    def create_connection(self, options):
        return redis.Redis(
            host=options['host'],
            port=options['port'],
            db=options['db'],
            password=options['password'],
            socket_timeout=options['expire']
        )

    def publish_subscribe(self):
        return self.connection.pubsub()

    def check_health(self):
        return self.connection.ping()


class DBConnection:
    def __init__(self, options):
        self.session = self.connect(options)

    def connect(self, options):
        engine = create_engine(options['url'])
        session = sessionmaker(bind=engine)
        meta = MetaData()
        meta.reflect(bind=engine)

        class Tasks:
            pass

        setattr(self, 'tasks', mapper(Tasks, meta.tables['task']))
        return session()
