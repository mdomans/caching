from settings import Settings


settings = Settings()

class MemcacheBackend:
    
    def __init__(self, *args, **kwargs):
        pass


def get_cache_backend():
    return {'memcache':MemcacheBackend,
            'mock': None, 
            }[settings.backend](settings)
        



