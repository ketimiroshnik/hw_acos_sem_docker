import random, string
import redis

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_redis():
    return redis.Redis(host="redis", port=6379, decode_responses=True)

def cache_url(r, short_id, url):
    r.set(short_id, url, ex=3600)

def get_cached_url(r, short_id):
    return r.get(short_id)