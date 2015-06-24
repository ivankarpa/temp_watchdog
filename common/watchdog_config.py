import configparser

from config import Config


class WatchdogConfig(Config):
    def __init__(self, file_name):
        default_values = configparser.ConfigParser({'port': '9091'})
        Config.__init__(self, file_name, default_values)
