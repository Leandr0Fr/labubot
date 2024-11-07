import time

from ..scraping.driver import DriverSingleton


def refresh():
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = 3
            retries = 3
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempts += 1
                    time.sleep(delay)
            DriverSingleton.get_driver().refresh()
            time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator
