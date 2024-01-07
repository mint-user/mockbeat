from django.contrib import admin
from django.contrib.admin import forms
from django.db import models
from django.forms import ModelForm

from mock_api.models import Service, Endpoint, Strategy
from mock_api.widjets import HtmlEditor


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint_id')
    # add_form_template = AppAdminForm
    formfield_overrides = {
        models.TextField: {
            'widget': HtmlEditor(
                attrs={
                    'rows': 50,
                    'cols': 200,
                    'class': 'python-editor',
                    'data-mimetype': 'text/x-python',
                    'style': 'height: 600px;',
                },
            ),
        },
    }

    # def formfield_for_dbfield(self, script_body, **kwargs):
    #     kwargs['initial'] = '123qwerty'
    #     return super().formfield_for_dbfield(script_body, **kwargs)

    def __init__(self, *args, **kwargs):
        # breakpoint()
        super().__init__(*args, **kwargs)
        breakpoint()
        # if self.instance and self.instance.is_active is not None:
        #     self.fields['is_active'].initial = 'Активен' if self.instance.is_active else 'Неактивен'
        self.instance.script_body = 'qwerty123'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'url_part', 'url', 'method')

    readonly_fields = ["url"]

    def has_add_permission(self, request):
        return Service.objects.count() >= 1
