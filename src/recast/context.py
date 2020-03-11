class Context(object):
    class LOG_LEVEL(object):
        ERROR = 1
        WARNING = 2
        PROGRESS = 100

    def log(self, level: LOG_LEVEL, info: str):
        pass

    def init(self):
        pass
