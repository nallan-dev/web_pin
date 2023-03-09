from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.urls import path

from conf.translations import t
from relay_app import views as relay_views

admin.AdminSite.site_title = " " + t("Switchers")
admin.AdminSite.site_header = t("Switchers - administration")
admin.AdminSite.index_title = t("")


admin.site.unregister(User)
admin.site.unregister(Group)


urlpatterns = [
    path("", relay_views.Index.as_view(), name="index"),
    path("describe_cron/", relay_views.DescribeCron.as_view()),
    path("settings/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
