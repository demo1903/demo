from redis import Redis

from swiper.cfg import REDIS

rds = Redis(**REDIS)
