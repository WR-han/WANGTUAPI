# TODO 修改token盐 数据库链接信息 抽离 settings.secret_key,settings.allowed_hosts
RBAC_token_salt = "RBAC_token"

project_database = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "wangtuapi",
        "USER": "root",
        "PASSWORD": "github377137470Tu",
        "HOST": "127.0.0.1",
        "PORT": "3306"
    }
}
project_secret_key = 'w1@2b=_rt&0ja(8n6a$6tq8+_xhfejfzfkjv4^3!_vp$-$gp++'
project_allowed_hosts = ["*"]

# 微信相关
# wechat_appid = ''
# wechat_secret = ''
# base_url = "https://api.weixin.qq.com/sns/jscode2session"
