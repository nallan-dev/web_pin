from django.apps import AppConfig

from conf.translations import t


class RelayAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "relay_app"
    verbose_name = t("Переключатели")
