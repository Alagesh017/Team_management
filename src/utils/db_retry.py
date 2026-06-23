import logging
import time
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from src import db


def is_mysql_gone_away_error(exception):

    if isinstance(exception, OperationalError):
        error_msg = str(exception).lower()
        gone_away_keywords = [
            "mysql server has gone away",
            "lost connection to mysql server",
            "server shutdown",
            "can't connect to mysql server"
        ]
        return any(keyword in error_msg for keyword in gone_away_keywords)
    return False


def db_retry(max_retries=3, initial_backoff=1.0):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError as e:
                    if is_mysql_gone_away_error(e):
                        retries += 1
                        if retries > max_retries:
                            logging.error(f"Max retries ({max_retries}) reached for MySQL gone away error. Aborting.")
                            raise
                        
                        try:
                            db.session.rollback()
                            db.session.remove()
                            logging.warning(f"MySQL connection lost. Retrying {retries}/{max_retries}...")
                        except Exception as rollback_err:
                            logging.warning(f"Error during rollback: {rollback_err}")
                        
                        backoff_time = initial_backoff * (2 ** (retries - 1))
                        time.sleep(backoff_time)
                    else:
                        raise
        return wrapper
    return decorator


def db_retry_context(func, max_retries=3, initial_backoff=1.0):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 0
        while retries <= max_retries:
            try:
                return func(*args, **kwargs)
            except SQLAlchemyError as e:
                if is_mysql_gone_away_error(e):
                    retries += 1
                    if retries > max_retries:
                        logging.error(f"Max retries ({max_retries}) reached for MySQL gone away error. Aborting.")
                        raise
                        
                    try:
                        db.session.rollback()
                        db.session.remove()
                        logging.warning(f"MySQL connection lost. Retrying {retries}/{max_retries}...")
                    except Exception as rollback_err:
                        logging.warning(f"Error during rollback: {rollback_err}")
                        
                    backoff_time = initial_backoff * (2 ** (retries - 1))
                    time.sleep(backoff_time)
                else:
                    raise
    return wrapper
