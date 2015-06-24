import unittest
import sys

sys.path.append('../common/')
import client_config


class ConfigParserTest(unittest.TestCase):
    CONFIG_WITH_GOOD_VALUES = './test_data/config_with_good_values.cfg'
    CONFIG_WITHOUT_PORT_VALUE = './test_data/config_without_port_value.cfg'
    CONFIG_WITHOUT_SECTION = './test_data/config_without_section.cfg'
    CONFIG_WITHOUT_OPTION = './test_data/config_without_option.cfg'
    NON_EXISTENT_CONFIG_FILE = './test_data/non_exist.cfg'

    def test_config_with_good_values(self):
        self.config = client_config.ClientConfig(self.CONFIG_WITH_GOOD_VALUES)
        test = self.config.get_option('connect', 'host')
        self.assertEqual(test[1], 'localhost')

    def test_default_port_value(self):
        self.config = client_config.ClientConfig(self.CONFIG_WITHOUT_PORT_VALUE)
        test = self.config.get_option('connect', 'port')
        self.assertEqual(test[1], '9091')

    def test_config_without_section(self):
        self.config = client_config.ClientConfig(self.CONFIG_WITHOUT_SECTION)
        test = self.config.get_option('connect', 'host')
        self.assertEqual(test[1], '')

    def test_config_without_option(self):
        self.config = client_config.ClientConfig(self.CONFIG_WITHOUT_OPTION)
        test = self.config.get_option('connect', 'host')
        self.assertEqual(test[1], '')

    def test_non_existent_config_file(self):
        self.config = client_config.ClientConfig(self.NON_EXISTENT_CONFIG_FILE)
        test = self.config.get_option('connect', 'host')
        self.assertEqual(test[0], False)


if __name__ == '__main__':
    unittest.main()
