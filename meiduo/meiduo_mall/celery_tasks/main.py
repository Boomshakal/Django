# celery运行的入口文件，用以启动celery
from celery import Celery


# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'


# 创建celery实例,可以指定别名
celery_app = Celery('meiduo_04')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 自动将异步任务添加到celery_app
celery_app.autodiscover_tasks([
    'celery_tasks.sms',
    'celery_tasks.email',
    'celery_tasks.html'

    ])

