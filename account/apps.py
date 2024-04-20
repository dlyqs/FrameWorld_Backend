from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'  # 这是应用的路径
    label = 'U'  # 新的唯一标签
    verbose_name = 'User Account Management'
