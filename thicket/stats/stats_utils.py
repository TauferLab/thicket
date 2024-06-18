from functools import wraps

import logging


def cache_stats_op(func):
    """Python decorator that handles insertion of stats operations in the thicket statsframe_ops_cache."""

    @wraps(func)
    def wrapper(thicket, *args, **kwargs):
        output_columns = func(thicket, *args, **kwargs)
        if func not in thicket.statsframe_ops_cache:
            thicket.statsframe_ops_cache[func] = {}

        for column in output_columns:
            thicket.statsframe_ops_cache[func][column] = (args, kwargs)
        return output_columns

    return wrapper


stats_logger = logging.getLogger("thicket.stats")

def stats_log(func):

    @wraps(func)
    def wrapper(thicket, *args, **kwargs):
        stats_logger.debug("About to call function {} with {} positional args (excluding the Thicket object) and {} kwargs".format(func.__name__, len(args), len(kwargs)))
        try:
            return func(thicket, *args, **kwargs)
        except Exception as e:
            stats_logger.debug("Caught error in {}: {}".format(func.__name__, str(e)))
            raise e
        
    return wrapper
