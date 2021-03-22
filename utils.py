import os
import logging
import functools

 
class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)
 
    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result
 

def create_logger():
    handler = logging.StreamHandler()
    formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)

    return root


def logger(func):
    @functools.wraps(func)
    def wrapper_logger(*args, **kwargs):
        logger = create_logger()
        try:
            return func(*args, **kwargs)
        except:
            err = "There was an exception in "
            err += func.__name__
            logger.exception(err)

            raise
    return wrapper_logger
