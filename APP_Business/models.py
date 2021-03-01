from django.db import models

from Module_Public.custom_model import BaseModel
from APP_RBAC.models import User


class UserAccount(BaseModel):
    """
    admin用户消费数据表
    """
    due_date = models.DateTimeField("存储有效期", auto_now_add=True)
    capacity = models.BigIntegerField("储存容量", default=0)
    now_data_size = models.BigIntegerField("现有总数据大小", default=0)
    data_money = models.PositiveIntegerField("剩余流量金额", default=0)
    admin_user = models.OneToOneField("APP_RBAC.User", on_delete=models.SET_DEFAULT, default="", db_constraint=False,
                                      blank=True, related_name="UserAccount", verbose_name="管理员账号")

    def __str__(self):
        return f"{self.admin_user.nickName}_消费数据"

    class Meta:
        db_table = 'Business_UserAccount'
        verbose_name = "admin用户消费数据表"
        verbose_name_plural = verbose_name
