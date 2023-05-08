from django.contrib import admin

from mock_api.models import Service, Endpoint, Strategy


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint_id', 'script_body')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):

    list_display = ('name', 'service', 'url_part', 'url', 'method')

    readonly_fields = ["url"]

    def has_add_permission(self, request):
        return Service.objects.count() >= 1
