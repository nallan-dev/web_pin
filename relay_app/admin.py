from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from conf.translations import t

from .models import BotConfig, PinData, ScheduleData


class PinDataAdmin(admin.ModelAdmin):
    list_display = (
        "command",
        "order_id",
        "board_num",
        "state",
        "invert_state",
        "visible",
    )
    fields = (
        ("order_id", "board_num"),
        ("visible", "invert_state"),
        "command",
        "comment",
    )
    list_filter = ("visible", "state")


class ScheduleDataAdmin(admin.ModelAdmin):
    list_display = ("action", "pin_name", "describe_cron", "active")
    list_filter = ("pin_data", "active")
    fields = (
        ("action", "pin_data"),
        ("cron_time", "describe_cron"),
        "comment",
        "active",
    )

    class Media:
        js = ["cron_slug.js"]

    @admin.display(description=t("Переключатель"))
    def pin_name(self, obj: ScheduleData) -> str:
        return obj.pin_data.command


class BotConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    list_editable = ("value",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return redirect(
            to=reverse(
                "admin:{0}_{1}_changelist".format(
                    self.model._meta.app_label,
                    self.model._meta.model_name,
                )
            )
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PinData, admin_class=PinDataAdmin)
admin.site.register(ScheduleData, admin_class=ScheduleDataAdmin)
if settings.USE_BOT:
    admin.site.register(BotConfig, admin_class=BotConfigAdmin)
