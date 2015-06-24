import socket
import threading
import sys

sys.path.append('../common/')
import watchdog_config


class Client(threading.Thread):
    def __init__(self, subprocess, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.sock = socket.socket()
        self.config = watchdog_config.WatchdogConfig('watchdog.cfg')
        self.subprocess = subprocess
        self.stop_signal = 1

    def run(self):
        try:
            host_found, host = self.config.get_option('connect', 'host')
            if not host_found:
                message = "Host not set in config"
                self.logger.error(message)
                return message
            _, port = self.config.get_option('connect', 'port')
            self.sock.bind((host, int(port)))
            self.sock.listen(1)
            while self.stop_signal:
                self.connection, self.address = self.sock.accept()
                command = self.receive_message()
                response = self.subprocess.execute_command(command)
                self.send_message(response)
        except ConnectionRefusedError:
            return "Connection to {0}:{1} refused".format(host, port)
        except socket.error as msg:
            return "Exception! errcode: {0}, message: {1}. Server: {2}:{3}".format(msg[0], msg[1], host, port)

    def stop(self):
        self.stop_signal = 0

    def send_message(self, message):
        self.connection.send(str(message).encode())

    def receive_message(self):
        return str(self.connection.recv(1024).decode())
