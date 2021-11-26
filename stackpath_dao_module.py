import datetime
import json
import redis
from dateutil import parser

from date_data_object_module import date_data_object


class stackpath_dao(object):
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    DB_NUMBER = "DB_NUMBER"

    def __init__(self, config):
        self.config = config
        host = self.config.get_properties_str(self.DB_HOST)
        port = self.config.get_properties_int(self.DB_PORT)
        db_number = self.config.get_properties_int(self.DB_NUMBER)
        self.redis_db_connection = redis.Redis(host, port, db=db_number, decode_responses=True)

    def insert_data_to_db(self, date_per_data_object, utc_datetime):
        try:
            requests_per_domain = date_per_data_object[utc_datetime]
            # save the data as json on redis
            json_requests_per_domain = json.dumps(requests_per_domain)
            json_utc_datetime = json.dumps(str(utc_datetime))
            self.redis_db_connection.set(json_utc_datetime, json_requests_per_domain)
        except Exception as e:
            raise Exception(e)

    def load_all_data(self):
        try:
            date_per_data_object = date_data_object()
            for json_utc_datetime in self.redis_db_connection.scan_iter(match='*'):
                # pull the dictionary which exist on specific utc datetime but in json
                # (because redis don't know what is date type, support on bytes by json format)
                requests_per_domain = json.loads(self.redis_db_connection.get(json_utc_datetime))
                # convert the utc datetime key from json to datetime
                utc_datetime = parser.parse(json.loads(json_utc_datetime))
                for domain, number_of_requests in requests_per_domain.items():
                    date_per_data_object.add_data(utc_datetime, domain, number_of_requests)
            return date_per_data_object
        except Exception as e:
            raise Exception(e)

    def clear_all_data(self):
        self.redis_db_connection.flushdb()
