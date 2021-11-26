from collections import OrderedDict


class date_data_object(object):
    def __init__(self):
        self.date_per_data = OrderedDict()

    def add_data(self, utc_datetime, domain, number_of_requests):
        if utc_datetime not in self.date_per_data.keys():
            self.date_per_data[utc_datetime] = {}
        if domain not in self.date_per_data[utc_datetime].keys():
            self.date_per_data[utc_datetime][domain] = number_of_requests
        else:
            self.date_per_data[utc_datetime][domain] += number_of_requests

    def sort_by_datetime_key(self):
        self.date_per_data = OrderedDict(sorted(self.date_per_data.items(), reverse=True))

    def get_all_data(self):
        return self.date_per_data
