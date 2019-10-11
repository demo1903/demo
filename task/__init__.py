import os

from celery import Celery

from task import config

# 作用:在当前的环境变量下面添加一个DJANGO_SETTINGS_MODULE的变量,帮助django找到settings文件的位置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

# 定义一个app
celery_app = Celery('worker')

# 从config中来进行配置
celery_app.config_from_object(config)

# autodiscover_tasks 用于查找django中都定义了哪些任务
celery_app.autodiscover_tasks()
