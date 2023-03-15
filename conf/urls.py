from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseNotFound, FileResponse
from django.urls import path

from conf.translations import t
from relay_app import views as relay_views

admin.AdminSite.site_title = " " + t("Switchers")
admin.AdminSite.site_header = t("Switchers - administration")
admin.AdminSite.index_title = t("")


admin.site.unregister(User)
admin.site.unregister(Group)


def serve_static(_, path):
    filepath = settings.STATIC_ROOT / path
    if not filepath.exists() or filepath.is_dir():
        return HttpResponseNotFound()
    else:
        return FileResponse(open(filepath, "rb"))


urlpatterns = [
    path("", relay_views.Index.as_view(), name="index"),
    path("describe_cron/", relay_views.DescribeCron.as_view()),
    path("settings/", admin.site.urls),
    path(settings.STATIC_URL[1:] + "<path:path>", serve_static, name="static"),
]
