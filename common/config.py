import configparser


class Config:
    def __init__(self, file_name, default_values):
        self.file_name = file_name
        self.config = default_values
        try:
            self.config.read(self.file_name)
        except configparser.MissingSectionHeaderError:
            pass

    def get_option(self, section, option):
        try:
            return True, str(self.config.get(section, option))
        except (configparser.NoOptionError, KeyError):
            return False, ""
        except (configparser.NoSectionError, KeyError):
            return False, ""
