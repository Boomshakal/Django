# 定义异步任务的文件，名字必须是tasks
from celery_tasks.main import celery_app

from . import constants
from .yuntongxun.sms import CCP


# 使用装饰器将以下任务装饰为异步任务

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """发送短信验证码异步任务"""

    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
