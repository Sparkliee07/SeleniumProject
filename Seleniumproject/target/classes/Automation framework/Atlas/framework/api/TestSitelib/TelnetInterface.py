import socket
import time
import threading

class TelnetConnection:
    WILL = 251
    WONT = 252
    DO = 253
    DONT = 254
    IAC = 255
    SGA = 3

    LOGIN = "login"
    PASSWORD = "Password"
    CMDPROMT = "$"
    EXITCMD = "exit"

    def __init__(self, hostname, port):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((hostname, port))
        self.tcp_socket.settimeout(0.1)
        self.timed_out = False
        self.timer = None

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self.tcp_socket:
            self.tcp_socket.close()
            self.tcp_socket = None

    def timer_event_handler(self):
        self.timed_out = True
        self.timer.cancel()

    def login_handler(self, username=None, password=None):
        if username and password:
            if not self.get_to_prompt(":", 2000):
                raise Exception("Failed to connect: no login prompt")
            self.write_line(username)
            if not self.get_to_prompt(":", 2000):
                raise Exception("Failed to connect: no password prompt")
            self.write_line(password)
            self.get_to_prompt(self.CMDPROMT, 2000)
        else:
            if not self.get_to_prompt("#", 2000):
                raise Exception("Failed to connect: no login prompt")

    def login(self, username=None, password=None, login_timeout_ms=10000):
        if username and password:
            login_thread = threading.Thread(target=self.login_handler, args=(username, password))
        else:
            login_thread = threading.Thread(target=self.login_handler)
        login_thread.start()
        login_thread.join(timeout=login_timeout_ms / 1000)

    def write_line(self, cmd):
        self.write(cmd + "\n")

    def write(self, cmd):
        if not self.tcp_socket:
            return
        buf = cmd.encode('ascii')
        self.tcp_socket.sendall(buf)

    def read(self, timeout_ms=100):
        if not self.tcp_socket:
            return None
        sb = []
        while True:
            self.parse_telnet(sb)
            time.sleep(timeout_ms / 1000)
            if self.tcp_socket is None or self.tcp_socket.gettimeout() == 0:
                break
        return ''.join(sb)

    def get_to_prompt(self, prompt, timeout_ms):
        self.timed_out = False
        self.timer = threading.Timer(timeout_ms / 1000, self.timer_event_handler)
        self.timer.start()
        sb = []
        while not self.timed_out:
            self.parse_telnet(sb)
            time.sleep(0.01)
            if ''.join(sb).strip().endswith(prompt):
                self.timer.cancel()
                return True
        self.timer.cancel()
        return False

    def parse_telnet(self, sb):
        try:
            while True:
                data = self.tcp_socket.recv(1)
                if not data:
                    break
                input = data[0]
                if input == self.IAC:
                    inputverb = self.tcp_socket.recv(1)[0]
                    if inputverb == self.IAC:
                        sb.append(chr(inputverb))
                    else:
                        inputoption = self.tcp_socket.recv(1)[0]
                        self.tcp_socket.sendall(bytes([self.IAC, self.WONT if inputverb == self.DO else self.DONT, inputoption]))
                else:
                    sb.append(chr(input))
        except socket.timeout:
            pass

    @property
    def is_connected(self):
        return self.tcp_socket and not self.timed_out
