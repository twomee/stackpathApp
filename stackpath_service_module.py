import datetime

from stackpath_dao_module import stackpath_dao


class stackpath_service_module(object):
    NUMBER_OF_DOMAINS = "NUMBER_OF_DOMAINS"
    HOUR_STATS = "HOUR_STATS"
    MINUTE_STATS = "MINUTE_STATS"

    def __init__(self, config):
        self.config = config
        self.dao = stackpath_dao(config)
        self.date_per_data_object = self.dao.load_all_data()
        print(self.date_per_data_object.get_all_data())

    def add_domain_requests(self, timestamp, content):
        try:
            utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
            del content["timestamp"]
            for domain, number_of_requests in content.items():
                self.date_per_data_object.add_data(utc_datetime, domain, number_of_requests)
                self.dao.insert_data_to_db(self.date_per_data_object.get_all_data(), utc_datetime)
        except Exception as e:
            raise Exception(e)

    def get_stats(self, stat_type):
        try:
            # get date range of now - from and until
            from_datetime, until_datetime = self.get_date_range(stat_type)
            # get the data between the date range of from and until
            requests_per_domain = self.get_data_between_date_range(from_datetime, until_datetime)
            # remove from the dictionary the domains with only one request
            requests_per_domain = self.remove_domains_with_one_request(requests_per_domain)
            # calculate the length we need to run for the stats
            length = self.length_for_stats(requests_per_domain)
            # create the stats from the top 10 items of the dictionary
            domain_stats = self.create_stat_per_domain(requests_per_domain, length)
            return domain_stats
        except Exception as e:
            raise Exception(e)

    def delete_all_data(self):
        self.dao.clear_all_data()

    def get_date_range(self, stat_type):
        try:
            utc_now = datetime.datetime.utcnow()
            hour_sats = self.config.get_properties_str(self.HOUR_STATS)
            if stat_type == hour_sats:
                from_datetime = utc_now.replace(microsecond=0, second=0, minute=0,
                                                hour=utc_now.hour) - datetime.timedelta(hours=1)
                until_datetime = utc_now.replace(second=0, microsecond=0, minute=0, hour=utc_now.hour)
            else:
                from_datetime = utc_now.replace(microsecond=0, second=0, minute=utc_now.minute,
                                                hour=utc_now.hour) - datetime.timedelta(minutes=1)
                until_datetime = utc_now.replace(second=0, microsecond=0, minute=utc_now.minute, hour=utc_now.hour)
            print(utc_now)
            print(from_datetime)
            print(until_datetime)
            return from_datetime, until_datetime
        except Exception as e:
            raise Exception(e)

    def get_data_between_date_range(self, from_datetime, until_datetime):
        try:
            requests_per_domain = {}
            self.date_per_data_object.sort_by_datetime_key()
            for datetime_key, domain_dict in self.date_per_data_object.get_all_data().items():
                if from_datetime < datetime_key < until_datetime:
                    for domain, number_of_requests in domain_dict.items():
                        if domain not in requests_per_domain.keys():
                            requests_per_domain[domain] = number_of_requests
                        else:
                            requests_per_domain[domain] += number_of_requests
            return requests_per_domain
        except Exception as e:
            raise Exception(e)

    def remove_domains_with_one_request(self, requests_per_domain):
        for domain in list(requests_per_domain.keys()):
            number_of_requests = requests_per_domain[domain]
            if number_of_requests < 2:
                del requests_per_domain[domain]
        return requests_per_domain

    def length_for_stats(self, requests_per_domain):
        try:
            number_of_domains = self.config.get_properties_int(self.NUMBER_OF_DOMAINS)
            if len(requests_per_domain) > number_of_domains:
                length = number_of_domains
            else:
                length = len(requests_per_domain)
            return length
        except Exception as e:
            raise Exception(e)

    def create_stat_per_domain(self, requests_per_domain, length):
        try:
            domain_stats = {}
            for domain, number_of_requests in list(requests_per_domain.items())[:length]:
                domain_stats[domain] = number_of_requests
            print(domain_stats)
            return domain_stats
        except Exception as e:
            raise Exception(e)
