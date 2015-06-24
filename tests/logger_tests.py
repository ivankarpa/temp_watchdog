import unittest
import sys

sys.path.append('../shared/')
import logger


class ConfigParserTest(unittest.TestCase):
    VALID_FILENAME = "test.log"
    INVALID_FILENAME = 'te\\0st.log'
    EMPTY_FILENAME = ''
    VALID_MESSAGE = 'Test message'
    EMPTY_MESSAGE = ''
    VALID_SEVERITY = 1
    EMPTY_SEVERITY = ''

    def setUp(self):
        pass

    def test_log_with_valid_data(self):
        log = logger.Logger()
        log.initialize(self.VALID_FILENAME)
        log.log_message(self.VALID_SEVERITY, self.VALID_MESSAGE)
        log.finalize()

    @unittest.SkipTest
    def test_log_with_invalid_filename(self):
        pass
    @unittest.SkipTest
    def test_log_with_empty_filename(self):
        pass
    @unittest.SkipTest
    def test_log_empty_message(self):
        pass


if __name__ == '__main__':
    unittest.main()
