import cron_descriptor
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from conf.translations import t
from relay_app.models import PinData, ScheduleData


class Index(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "title": t("Переключатели"),
            "no_switches": t("Здесь пока нет переключателей - настройте их"),
            "updated": t("Обновлено"),
            "schedule_tasks_title": t("Плановые задачи"),
            "pin_data": [
                pin.as_dict() for pin in PinData.objects.filter(visible=True)
            ],
            "schedule_data": [
                schedule.as_dict() for schedule in ScheduleData.objects.all()
            ],
        }
        template = (
            "pin_content.html" if "ajax" in request.GET else "index.html"
        )
        return render(request, template, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        pin_id = int(request.POST.get("pin_id", "0"))  # noqa
        schedule_id = int(request.POST.get("schedule_id", "0"))  # noqa
        state_to = bool(int(request.POST.get("state")))  # noqa
        if pin_id:
            pin = get_object_or_404(PinData, id=pin_id)
            pin.switch(state_to)
            return HttpResponse(status=200)
        elif schedule_id:
            schedule = get_object_or_404(ScheduleData, id=schedule_id)
            schedule.active = state_to
            schedule.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class DescribeCron(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cron_str = request.GET.get("cron_str", "")  # noqa

        try:
            cron_description = cron_descriptor.get_description(
                cron_str, settings.CRON_OPTIONS
            )
        except Exception:
            cron_description = t("Невалидный Крон")
        return JsonResponse(
            data={"cron_description": cron_description},
            safe=False,
            json_dumps_params={"indent": 4, "ensure_ascii": False},
        )
