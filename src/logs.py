
from enum import IntEnum
import logging
import threading


class LEVELS(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

class Logs:
    _instance = None
    _lock = threading.Lock()
    
    _logs = None
    _level = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logs is None:
            self._logs = logging.getLogger("ThreesBot")
            self.setLevel(logging.INFO)
    
    def shutdown(self):
        if self._logs is not None:
            self._logs = None
            self._level = None

    def setLevel(self, level):
        if self._logs is not None:
            self._logs.setLevel(level)
            self._level = level

    def getInfo(self, msg):
        if self._logs is not None:
            self._logs.info(msg)
        if self._level == logging.DEBUG:
            self._printMessage(msg, logging.INFO)
    
    def getWarning(self, msg):
        if self._logs is not None:
            self._logs.warning(msg)
        if self._level == logging.DEBUG:
            self._printMessage(msg, logging.WARNING)

    def getError(self, msg):
        if self._logs is not None:
            self._logs.error(msg)
        if self._level == logging.DEBUG:
            self._printMessage(msg, logging.ERROR)

    def _printMessage(self, msg="", level=logging.INFO):
        match level:
            case logging.DEBUG:
                print(f"Debug:::::::{msg}")
            case logging.INFO:
                print(f"Info::::::::{msg}")
            case logging.WARNING:
                print(f"Warning:::::{msg}")
            case logging.ERROR:
                print(f"Error:::::::{msg}")
            case _:
                print(f"Log:::::::::{msg}")

logs = Logs()
