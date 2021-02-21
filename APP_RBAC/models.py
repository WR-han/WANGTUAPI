from django.db import models

from Module_Public.custom_model import AccountModel, BaseModel


class User(AccountModel):
    """
    用户
    """
    superior = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="lowerLevel",
                                 verbose_name="上级", db_constraint=False)
    Identity = models.ManyToManyField("APP_RBAC.Identity", verbose_name="身份", through="APP_RBAC.UserIdentity",
                                      related_name="User")
    Permissions = models.ManyToManyField("APP_RBAC.Permissions", verbose_name="权限",
                                         through="APP_RBAC.UserPermissions", related_name="User")

    @property
    def get_permissions(self):
        """
        获取所有权限 个人权限+身份权限
        :return: 用户所有权限
        """
        my_permissions = [my_pm.codeName for my_pm in self.Permissions.all()]
        my_identity = self.Identity.all()
        identity_permission = []
        for dep in my_identity:
            identity_permission += [dep_pm.codeName for dep_pm in dep.Permissions.all()]
        my_permissions += identity_permission
        return my_permissions

    def __str__(self):
        return f"用户_{self.nickName}"

    class Meta:
        db_table = 'RBAC_User'
        verbose_name = "1.用户表"
        verbose_name_plural = verbose_name


class Identity(BaseModel):
    """
    身份&部门&岗位
    """

    # classifyChoices = ((1, "业务部门"), (2, "行政部门"))

    superior = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="lowerLevel",
                                 verbose_name="上级", db_constraint=False)
    Permissions = models.ManyToManyField("APP_RBAC.Permissions", verbose_name="权限",
                                         through="APP_RBAC.IdentityPermissions", related_name="Identity")

    name = models.CharField("名称", max_length=15, unique=True)

    # classify = models.BooleanField("类型", choices=classifyChoices, default=1)

    def __str__(self):
        return f"身份_{self.name}"

    class Meta:
        db_table = 'RBAC_Identity'
        verbose_name = "2.身份表"
        verbose_name_plural = verbose_name


class Permissions(BaseModel):
    """
    权限表
    """

    name = models.CharField("权限名称", max_length=15)
    codeName = models.CharField("权限代码", max_length=30)

    def __str__(self):
        return f"权限_{self.name}"

    class Meta:
        db_table = 'RBAC_Permissions'
        verbose_name = "3.权限表"
        verbose_name_plural = verbose_name


class UserIdentity(BaseModel):
    """
    用户/身份关系表
    """

    User = models.ForeignKey("APP_RBAC.User", on_delete=models.CASCADE, verbose_name="用户",
                             related_name="UserIdentity", db_constraint=False)
    Identity = models.ForeignKey("APP_RBAC.Identity", on_delete=models.CASCADE, verbose_name="身份",
                                 related_name="UserIdentity", db_constraint=False)

    def __str__(self):
        return f"{self.Identity.name}_{self.User.nickName}"

    class Meta:
        db_table = 'RBAC_User_Identity'
        verbose_name = "4.用户/身份关系表"
        verbose_name_plural = verbose_name


class UserPermissions(BaseModel):
    """
    用户权限表
    """

    User = models.ForeignKey("APP_RBAC.User", on_delete=models.CASCADE, verbose_name="用户",
                             related_name="UserPermissions", db_constraint=False)
    Permissions = models.ForeignKey("APP_RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="UserPermissions", db_constraint=False)

    def __str__(self):
        return f"{self.User.nickName}_{self.Permissions.name}"

    class Meta:
        db_table = 'RBAC_User_Permissions'
        verbose_name = "5.用户权限"
        verbose_name_plural = verbose_name


class IdentityPermissions(BaseModel):
    """
    身份基础权限
    """

    Identity = models.ForeignKey("APP_RBAC.Identity", on_delete=models.CASCADE, verbose_name="身份",
                                 related_name="IdentityPermissions", db_constraint=False)
    Permissions = models.ForeignKey("APP_RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="IdentityPermissions", db_constraint=False)

    def __str__(self):
        return f"{self.Identity.name}_{self.Permissions.name}"

    class Meta:
        db_table = 'RBAC_Identity_Permissions'
        verbose_name = "6.身份基础权限"
        verbose_name_plural = verbose_name
