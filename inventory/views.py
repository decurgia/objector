import json
import logging
from secrets import compare_digest
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import AutoPermissionRequiredMixin
from .models import Location, Object, Sensor
from maintenance.models import Task, Journal, Trigger
from .forms import ObjectForm
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from jsonpath_ng import parse
from .filters import LocationFilter, ObjectFilter, SensorFilter

logger = logging.getLogger(__name__)


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_group__in=groups_as_list)
            | Location.objects.filter(maintenance_group__in=groups_as_list)
        )
        filterset = LocationFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        filterset = LocationFilter(self.request.GET, queryset=self.queryset)
        context["filter"] = filterset
        return context


class LocationCreateView(AutoPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Location
    fields = [
        "name",
        "description",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_group",
        "maintenance_group",
    ]
    success_message = _("%(name)s was created successfully")

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["management_group"] = int(
            self.request.GET.get("management_group", False)
        )
        initial["maintenance_group"] = int(
            self.request.GET.get("maintenance_group", False)
        )
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LocationDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Location
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_list"] = Object.objects.filter(location=self.object.id)
        return context


class LocationUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Location
    raise_exception = True
    fields = [
        "name",
        "description",
        "image",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_group",
        "maintenance_group",
    ]

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LocationDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Location
    raise_exception = True
    success_url = reverse_lazy("inventory:location-list")


class ObjectListView(LoginRequiredMixin, ListView):
    model = Object
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )
        filterset = ObjectFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super(ObjectListView, self).get_context_data(**kwargs)
        filterset = ObjectFilter(self.request.GET, queryset=self.queryset)
        context["filter"] = filterset
        return context


class ObjectCreateView(AutoPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Object
    form_class = ObjectForm
    success_message = _("%(name)s was created successfully")

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["location"] = int(self.request.GET.get("location", False))
        initial["management_group"] = int(
            self.request.GET.get("management_group", False)
        )
        initial["maintenance_group"] = int(
            self.request.GET.get("maintenance_group", False)
        )
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ObjectDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Object
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Task.objects.filter(object=self.object.id)
        context["sensor_list"] = Sensor.objects.filter(object=self.object.id)
        return context


class ObjectUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Object
    raise_exception = True
    form_class = ObjectForm

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ObjectDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Object
    raise_exception = True
    success_url = reverse_lazy("inventory:object-list")


class SensorListView(LoginRequiredMixin, ListView):
    model = Sensor
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Sensor.objects.filter(object__owner=self.request.user)
            | Sensor.objects.filter(object__management_group__in=groups_as_list)
            | Sensor.objects.filter(object__maintenance_group__in=groups_as_list)
        )
        filterset = SensorFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super(SensorListView, self).get_context_data(**kwargs)
        filterset = SensorFilter(self.request.GET, queryset=self.queryset)
        context["filter"] = filterset
        return context


class SensorCreateView(AutoPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sensor
    fields = [
        "name",
        "description",
        "image",
        "object",
    ]
    success_message = _("%(name)s was created successfully")

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["object"] = int(self.request.GET.get("object", False))
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SensorDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Sensor
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trigger_list"] = Trigger.objects.filter(sensor=self.object.id)
        return context


class SensorUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Sensor
    raise_exception = True
    fields = [
        "name",
        "description",
        "image",
        "object",
        "webhook_authorization",
        "webhook_payload",
        "status",
    ]

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SensorDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Sensor
    raise_exception = True
    success_url = reverse_lazy("inventory:location-list")


@method_decorator(csrf_exempt, name="dispatch")
class SensorWebhookView(SingleObjectMixin, View):
    model = Sensor

    def post(self, request, *args, **kwargs):
        header_authorization = request.headers.get("Authorization", False)
        if not header_authorization:
            return HttpResponseForbidden(
                "Authorization not found in header.",
                content_type="text/plain",
            )

        self.object = self.get_object()
        webhook_authorization = self.object.webhook_authorization

        if not webhook_authorization:
            return HttpResponseForbidden(
                "No webhook authorization value specified on sensor.",
                content_type="text/plain",
            )

        if not compare_digest(webhook_authorization, header_authorization):
            return HttpResponseForbidden(
                "Incorrect Authorization value.",
                content_type="text/plain",
            )

        try:
            self.object.webhook_payload = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest(
                "Message contains invalid JSON.", content_type="text/plain"
            )

        self.object.status = self.get_sensor_status()
        self.object.save()
        return HttpResponse("Webhook payload saved.", content_type="text/plain")

    def get_sensor_status(self) -> int:
        sensor_status = Sensor.Statuses.GREEN

        triggers = Trigger.objects.filter(sensor=self.object.id)
        for trigger in triggers:
            logger.info(f"Trigger: {trigger.name}")

            trigger.status = Trigger.Statuses.GREEN
            trigger_sensor_value = ""
            jsonpath_expression = parse(trigger.jsonpath_expression)

            for match in jsonpath_expression.find(self.object.webhook_payload):

                logger.info(f"Match value: {match.value}")
                logger.info(f"Trigger condition: {trigger.condition}")
                logger.info(f"Trigger amber value: {trigger.amber_value}")
                logger.info(f"Trigger red value: {trigger.red_value}")

                if (
                    (
                        Trigger.Conditions.EQUALS == trigger.condition
                        and match.value == trigger.red_value
                        and Trigger.Statuses.RED < trigger.status
                    )
                    or (
                        Trigger.Conditions.NOTEQUALS == trigger.condition
                        and match.value != trigger.red_value
                        and Trigger.Statuses.RED < trigger.status
                    )
                    or (
                        Trigger.Conditions.LESSTHAN == trigger.condition
                        and float(match.value) < float(trigger.red_value)
                        and Trigger.Statuses.RED < trigger.status
                    )
                    or (
                        Trigger.Conditions.LESSTHANOREQUALTO == trigger.condition
                        and float(match.value) <= float(trigger.red_value)
                        and Trigger.Statuses.RED < trigger.status
                    )
                    or (
                        Trigger.Conditions.GREATERTHAN == trigger.condition
                        and float(match.value) > float(trigger.red_value)
                        and Trigger.Statuses.RED < trigger.status
                    )
                    or (
                        Trigger.Conditions.GREATERTHANOREQUALTO == trigger.condition
                        and float(match.value) >= float(trigger.red_value)
                        and Trigger.Statuses.RED < trigger.status
                    )
                ):
                    trigger_sensor_value = match.value
                    trigger.status = Trigger.Statuses.RED
                    sensor_status = Sensor.Statuses.RED

                elif (
                    (
                        Trigger.Conditions.EQUALS == trigger.condition
                        and match.value == trigger.amber_value
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                    or (
                        Trigger.Conditions.NOTEQUALS == trigger.condition
                        and match.value != trigger.amber_value
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                    or (
                        Trigger.Conditions.LESSTHAN == trigger.condition
                        and float(match.value) < float(trigger.amber_value)
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                    or (
                        Trigger.Conditions.LESSTHANOREQUALTO == trigger.condition
                        and float(match.value) <= float(trigger.amber_value)
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                    or (
                        Trigger.Conditions.GREATERTHAN == trigger.condition
                        and float(match.value) > float(trigger.amber_value)
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                    or (
                        Trigger.Conditions.GREATERTHANOREQUALTO == trigger.condition
                        and float(match.value) >= float(trigger.amber_value)
                        and Trigger.Statuses.AMBER < trigger.status
                    )
                ):
                    trigger_sensor_value = match.value
                    trigger.status = Trigger.Statuses.AMBER
                    sensor_status = Sensor.Statuses.AMBER

                elif Trigger.Statuses.GREEN == trigger.status:
                    trigger_sensor_value = match.value

            trigger.sensor_value = trigger_sensor_value
            trigger.save()

        logger.info(f"New sensor status: {sensor_status}")
        return sensor_status
