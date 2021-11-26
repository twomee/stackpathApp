from jproperties import Properties


class properties_object:
    def __init__(self):
        self.config = Properties()

    def load_properties(self):
        try:
            with open('config.properties', 'rb') as read_prop:
                self.config.load(read_prop)
        except Exception as e:
            raise Exception(e)

    def get_properties_int(self, name):
        try:
            return int(self.config.get(name).data)
        except Exception as e:
            raise Exception(e)

    def get_properties_str(self, name):
        try:
            return self.config.get(name).data
        except Exception as e:
            raise Exception(e)
