import datetime
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
    print('sid_list:', sid_list)
    # 筛选出匹配的用户
    users = User.objects.filter(
        sex=profile.dating_sex,
        location=profile.dating_location,
        birth_day__gt=earliest_birthday,  # 大于
        birth_day__lt=latest_birthday,  # 小于
    ).exclude(id__in=sid_list)[:20]  # 排除已经取过的用户,并且进行切片每次取20个
    return users


def like_someone(user, sid):
    """喜欢某人"""

    Swiped.swipe(user.id, sid, 'like')  # 添加滑动记录

    # 检查对方是否喜欢过自己
    if Swiped.is_liked(sid, user.id):
        # TODO:如果对方喜欢过自己,匹配成好友
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False
