import datetime

loggers = {}
longest_name = 0


class Logger:
    longest_level = 8

    def __init__(self, name) -> None:
        self.name = name

    def _format(self, level, message):
        global longest_name
        time = str(datetime.datetime.now())[:-7]
        level = level.upper() + " " * (self.longest_level - len(level))
        name = self.name + " " * (longest_name - len(self.name))
        return f"[{time}] [{level}] {name} | {message}"

    def log(self, level, message):
        print(self._format(level, message))

    def debug(self, message):
        self.log("debug", message)

    def info(self, message):
        self.log("info", message)

    def warning(self, message):
        self.log("warning", message)

    def warn(self, message):
        self.log("warning", message)

    def error(self, message):
        self.log("error", message)

    def critical(self, message):
        self.log("critical", message)


def getLogger(name):
    global longest_name
    if name in loggers.keys():
        return loggers[name]

    if len(name) > longest_name:
        longest_name = len(name)

    logger = Logger(name)
    loggers.update({name: logger})

    return logger


if __name__ == '__main__':
    logger1 = getLogger(__name__)
    logger2 = getLogger("short")

    logger1.info("idk long info")
    logger2.warn("short warn")
