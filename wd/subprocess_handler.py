import os
import subprocess
import signal
import threading
import time
import sys

sys.path.append('../common/')
import watchdog_config


class Subprocess(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.process_id = None
        self.config = watchdog_config.WatchdogConfig('../wd/watchdog.cfg')
        _, self.subprocess_file = self.config.get_option('subprocess', 'subprocess_file')
        self.stop_signal = 1

    def run(self):
        while self.stop_signal:
            if self.process_id:
                if self.pipe.poll() is not None:
                    self.process_id = None
                    while self.process_id is None:
                        self.start_subprocess()
            time.sleep(1)
        self.stop_subprocess

    def stop(self):
        self.stop_signal = 0

    def start_subprocess(self):
        if self.process_id is not None:
            message = "Subprocess is already started. PID: {0}".format(self.process_id)
            self.logger.error(message)
            self.logger.finalize()
            return message
        else:
            self.file = "../subprocess/" + self.subprocess_file
            self.pipe = subprocess.Popen([sys.executable, self.file])
            if self.pipe.pid is not None:
                self.process_id = self.pipe.pid
                return "Subprocess successfully started. PID: {0}".format(self.process_id)
            else:
                return "Unsuccessful attempt to start subprocess"

    def stop_subprocess(self):
        if self.process_id:
            try:
                os.kill(self.process_id, signal.SIGTERM)
                self.pipe.wait(3)
            except subprocess.TimeoutExpired:
                os.kill(self.process_id, signal.SIGKILL)
            self.process_id = None
            return "Subprocess stopped"
        else:
            return "Subprocess not started"

    def subprocess_status(self):
        if self.process_id:
            return "Subprocess is started. PID: {0}".format(self.process_id)
        else:
            return "Subprocess not started"

    def execute_command(self, command):
        if command == "start":
            return self.start_subprocess()
        elif command == "stop":
            return self.stop_subprocess()
        elif command == "status":
            return self.subprocess_status()
