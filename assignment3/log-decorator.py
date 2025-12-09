#Task 1

import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        logger.info(f"function: {func.__name__}")

        if args:
            logger.info(f"positional parameters: {args}")
        else:
            logger.info("positional parameters: none")

        if kwargs:
            logger.info(f"keyword parameters: {kwargs}")
        else:
            logger.info("keyword parameters: none")
        
        result = func(*args, **kwargs)

        logger.info(f"return value: {result}")
        logger.info("---")

        return result
    return wrapper

@logger_decorator
def hello_world():
    print("Hello, World!")

@logger_decorator
def takes_postional(*args):
    return True

@logger_decorator
def takes_keyword(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    hello_world()
    takes_postional(1, 2, 3, "apple")
    takes_keyword(a=10, b="banana")
    