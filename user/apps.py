from django.apps import AppConfig

# 单个app的config，需要添加到settings.py中
# 注意这里的verbose_name是admin界面中的显示名称
class UserConfig(AppConfig):
    name = 'user'
    verbose_name = '用户'