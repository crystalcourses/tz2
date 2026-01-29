from django.core.cache import cache

USERS_LIST_CACHE_KEY = 'users_list'
USER_CACHE_KEY = 'user_{}'
CACHE_TTL = 60 * 15


class UserCacheService:
    @staticmethod
    def get_users_list():
        return cache.get(USERS_LIST_CACHE_KEY)

    @staticmethod
    def set_users_list(data):
        cache.set(USERS_LIST_CACHE_KEY, data, CACHE_TTL)

    @staticmethod
    def get_user(user_id):
        return cache.get(USER_CACHE_KEY.format(user_id))

    @staticmethod
    def set_user(user_id, data):
        cache.set(USER_CACHE_KEY.format(user_id), data, CACHE_TTL)

    @staticmethod
    def invalidate():
        cache.delete(USERS_LIST_CACHE_KEY)

    @staticmethod
    def invalidate_user(user_id):
        cache.delete(USER_CACHE_KEY.format(user_id))
        cache.delete(USERS_LIST_CACHE_KEY)