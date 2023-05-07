from django.contrib import admin
from django.db.models import Model

from mock_api.models import Service, Endpoint


# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):

    list_display = ('name', 'service', 'url_part', 'url', 'method')

    readonly_fields = ["url"]

    def has_add_permission(self, request):
        return Service.objects.count() >= 1
