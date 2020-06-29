import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import defaultdict



class Redis:
    def __init__(self, options):
        for k,v in options.items():
            print(k, v)
        self.connection = self.create_connection(options)
    
    def create_connection(self, options):
        return redis.StrictRedis(
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
        self.connection = self.connect(options)

    def connect(self, options):
        engine = create_engine(options['uri'])
        session = sessionmaker(bind=engine)
        return session

