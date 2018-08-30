from django.apps import AppConfig


class WritingConfig(AppConfig):
    name = 'writing'

    def ready(self):
        # import signal handler
        import writing.signals

