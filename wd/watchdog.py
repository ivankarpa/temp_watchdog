import sys

import client_handler
import subprocess_handler
from daemon import Daemon

sys.path.append('../common/')
import watchdog_config

sys.path.append('../shared/')
import logger


class Watchdog(Daemon):
    def __init__(self, pid_file):
        Daemon.__init__(self, pid_file)
        self.logger = logger.Logger()
        self.logger.initialize("DDD.log")
        self.subprocess = subprocess_handler.Subprocess(self.logger)
        self.client = client_handler.Client(self.subprocess,self.logger)

    def run(self):
        self.subprocess.start()
        self.client.start()

    def pause(self):
        self.subprocess.stop()
        self.client.stop()


if __name__ == '__main__':
    config = watchdog_config.WatchdogConfig('watchdog.cfg')
    pid_file_found, pid_file = config.get_option('daemon', 'pid_file')
    if not pid_file_found:
        sys.exit("pid file not set in config")

    watchdog = Watchdog(pid_file)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            watchdog.start()
        elif 'stop' == sys.argv[1]:
            watchdog.pause()
            watchdog.stop()

        elif 'restart' == sys.argv[1]:
            watchdog.restart()
        elif 'status' == sys.argv[1]:
            pid = watchdog.get_pid()
            if pid:
                print('Watchdog is running [{0}]'.format(pid))
            else:
                print('Watchdog is stopped')
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)
