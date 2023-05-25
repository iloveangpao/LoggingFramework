import logging 
import logging.handlers
import inspect
import types

class LoggingMeta(type):

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        for attr_name, attr_value in instance.__class__.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                modified_method = dummy(kwargs['name'], attr_value, kwargs['filename'], filter = kwargs['filter'])
                setattr(instance, attr_name, types.MethodType(modified_method, instance))
        return instance


def dummy(name, func, filename = 'log.txt', level=logging.INFO, message=None, filter = logging.INFO):
    def wrapper(*args, **kwargs):
        print(dir(func))
        logger = logging.getLogger(name)
        setup_logger(logger = logger, file_path = filename, log_level=filter, max_lines=10, backup_count=10) 
        log_message = message if message else f"Calling {func.__name__}"
        logger.log(level, log_message)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.exception("Exception occurred")
            raise
        else:
            logger.log(level, f"{func.__name__} returned: {result}")
            return result
    return wrapper

class LineRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, mode='a', maxLines=0, backupCount=0, encoding=None, delay=1):
        self.maxLines = maxLines
        self.filename = filename
        super().__init__(filename, mode, maxBytes=0, backupCount=backupCount, encoding=encoding, delay=delay)

    def emit(self, record):
        count = 0
        
        super().emit(record)
        try:
            with open(self.filename, 'r') as f:
                for count, line in enumerate(f):
                    pass
        except PermissionError:
            pass
        if count > self.maxLines:
            try:
                self.doRollover()
            except PermissionError:
                pass

def setup_logger(logger = logging.getLogger(), file_path=None, log_level=logging.INFO, max_lines=0, backup_count=0):
    logger = logger
    logger.setLevel(logging.DEBUG)

    if file_path:
        file_handler = LineRotatingFileHandler(file_path, maxLines=max_lines, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        file_handler.addFilter(LevelFilter(log_level))
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level


