import time
import datetime
import json
from threading import Thread, Timer
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout

class Request:
    def __init__(self, url, parameters, headers, auth):
        self.url = url
        self.parameters = parameters
        self.headers = headers
        self.auth = auth
        self.session = self.create_session()

    def create_session(self):
        session = Session()
        seession.headers.update(self.headers)
        return session
    
    def make_get_request(self):
        return self.session.get(self.url, params=self.parameters)
