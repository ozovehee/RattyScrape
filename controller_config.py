import json

SUPPORTED_CONFIG_KEYS = ["driver_options", "engine", "proxies", "logging_file"]

class InvalidConfigError(Exception):
    def __init__(self, message=f"Only the following config options are supported: {SUPPORTED_CONFIG_KEYS}"):
        self.message = message
        super().__init__(self.message)

class ControllerConfig():

    def __init__(self, config={}):
        if not config:
            # Read the JSON file to get the logging file path
            with open("default_config.json", 'r') as file:
                self.config = json.load(file)
        else:
            self.config = config

    def get_config(self):
        return self.config
    
    def replace_config(self, new_config):
        self.config = new_config

    def get_config_value(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return None
    
    def set_config_value(self, key, value):
        if key not in SUPPORTED_CONFIG_KEYS:
            raise InvalidConfigError
        self.config[key] = value        

