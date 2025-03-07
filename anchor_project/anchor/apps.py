from django.apps import AppConfig

class AnchorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anchor'

    def ready(self):
        from polaris.integrations import register_integrations
        from .sep1 import toml

        register_integrations(
            toml=toml,
        )