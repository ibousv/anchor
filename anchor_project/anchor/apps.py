from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'anchor'

    def ready(self):
        # import integrations
        from polaris.integrations import register_integrations
        
        register_integrations(
           # refer to the APIs to see required fields
        )

