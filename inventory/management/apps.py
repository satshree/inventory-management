from django.apps import AppConfig


class ManagementConfig(AppConfig):
    name = 'management'

    def ready(self):
        from . import signals
        super(ManagementConfig, self).ready()
