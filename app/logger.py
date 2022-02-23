from datetime import datetime

class Logger:
    DEFAULT = '\033[0m'
    WARNING = '\033[93m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    DETECTION = '\033[94m'
    
    def _date():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def message(text):
        print(Logger._date() + ' [INFO] ' + text)

    @staticmethod
    def success(text):
        print(Logger.SUCCESS + Logger._date() + ' [SUCCESS] ' +  text + Logger.DEFAULT)

    @staticmethod
    def error(text):
        print(Logger.ERROR + Logger._date() + ' [ERROR] ' + text + Logger.DEFAULT)

    @staticmethod
    def warning(text):
        print(Logger.WARNING + Logger._date() + ' [WARNING] ' + text + Logger.DEFAULT)

    @staticmethod
    def detection(text):
        print(Logger.DETECTION + Logger._date() + ' [DETECTION] ' + text + Logger.DEFAULT)