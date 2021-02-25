from Module_Public.custom_Permission import MainPermission, SecondaryPermission


class UserPermission(MainPermission):
    """
    全部学生信息
    """
    pass


class DepartmentPermission(SecondaryPermission):
    """
    所在部门旗下学生信息
    """
    pass
