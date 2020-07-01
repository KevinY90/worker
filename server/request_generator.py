import time
import datetime
import json
from threading import Thread, Timer
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout


class Request:
    def __init__(self, url, parameters, headers):
        self.url = url
        self.parameters = self.parse_request_options(parameters) if parameters else ''
        self.headers = self.parse_request_options(headers) if headers else ''
        self.session = self.create_session()

    def create_session(self):
        session = Session()
        if self.headers:
            session.headers.update(self.headers)
        return session

    def parse_request_options(self, options_str):
        opt = {}
        items = options_str.split(',')
        for p in items:
            k,v = p.split('=')
            opt[k] = v
        return opt
    
    def make_get_request(self):
        return self.session.get(self.url, params=self.parameters)
