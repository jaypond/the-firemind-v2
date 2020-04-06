from datetime import datetime
from functools import wraps

def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = datetime.utcnow()
        result = f(*args, **kwargs)
        end = datetime.utcnow()
        print('%s: %s' % (f.__name__, (end - start).total_seconds()))
        return result
    return wrapper

def atimer(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        start = datetime.utcnow()
        result = await f(*args, **kwargs)
        end = datetime.utcnow()
        print('%s: %s' % (f.__name__, (end - start).total_seconds()))
        return result
    return wrapper
