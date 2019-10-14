import datetime
import time

from libs.cache import rds
from common import keys
from user.models import User
from social.models import Swiped, Friend


def rcmd(user):
    """推荐可滑动的用户"""
    profile = user.profile
    print(profile)

    # 获取当前日期
    today = datetime.date.today()

    # 最早出生日期
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)

    # 最晚出生日
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 取出滑过的用户 ID
    sid_list = Swiped.objects.filter(uid=user.id).values_list('sid', flat=True)

    # 取出超级喜欢过自身,但是还没有被自己滑动过的用户ID
    # 使用ORM取出的方式
    # who_superlike_me = Swiped.objects.filter(sid=user.id, stype='superlike') \
    #                                  .exclude(uid__in=sid_list) \
    #                                  .values_list('uid', flat=True)

    # 使用redis取出
    superliked_me_id_list = [int(uid) for uid in rds.zrange(keys.SUPERLIKED_KET.format(user.id), 0, 19)]
    superliked_me_users = User.objects.filter(id__in=superliked_me_id_list)

    # 筛选出匹配的用户
    other_count = 20 - len(superliked_me_users)
    if other_count > 0:
        other_users = User.objects.filter(
            sex=profile.dating_sex,
            location=profile.dating_location,
            birth_day__gt=earliest_birthday,  # 大于
            birth_day__lt=latest_birthday,  # 小于
        ).exclude(id__in=sid_list)[:20]  # 排除已经取过的用户,并且进行切片每次取20个
        users = superliked_me_users | other_users
    else:
        users = superliked_me_users
    return users


def like_someone(user, sid):
    """喜欢某人"""

    Swiped.swipe(user.id, sid, 'like')  # 添加滑动记录

    # 检查对方是否喜欢过自己
    if Swiped.is_liked(sid, user.id):
        # 如果对方喜欢过自己,匹配成好友
        Friend.make_friend(user.id, sid)
        # 如果对方超级喜欢过你,将对方从你的超级喜欢推荐列表中删除
        rds.zrem(keys.SUPERLIKED_KET.format(user.id), sid)
        return True
    else:
        return False


def superlike_someone(user, sid):
    """
    超级喜欢某人

    超级喜欢过对方,则一定会出现在对方的推荐列表里
    """
    Swiped.swipe(user.id, sid, 'superlike')  # 添加滑动记录

    # 将自己的ID写入到对方的优先推荐队列
    rds.zadd(keys.SUPERLIKED_KET.format(sid), {user.id: time.time()})

    # 检查对方是否喜欢过自己
    if Swiped.is_liked(sid, user.id):
        # 如果对方喜欢过自己,匹配成好友
        Friend.make_friend(user.id, sid)
        # 如果对方超级喜欢过你,将对方从你的超级喜欢推荐列表中删除
        rds.zrem(keys.SUPERLIKED_KET.format(user.id), sid)
        return True
    else:
        return False
