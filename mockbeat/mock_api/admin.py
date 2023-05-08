from django.contrib import admin
from django.contrib.admin import forms
from django.db import models
from django.forms import ModelForm

from mock_api.models import Service, Endpoint, Strategy
from mock_api.widjets import HtmlEditor


# class AppAdminForm(ModelForm):
#     model = Strategy
#
#     class Meta:
#         fields = ('script_body',)
#         widgets = {
#             'code': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
#             # 'code': HtmlEditor(attrs={'style': 'width: 90%; height: 1000;'}),
#         }

# class MyModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 100})},
#     }
#
# admin.site.register(MyModel, MyModelAdmin)


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint_id', 'script_body')
    # add_form_template = AppAdminForm
    formfield_overrides = {
        models.TextField: {'widget': HtmlEditor(attrs={'rows': 50, 'cols': 200, 'class': 'python-editor', 'data-mimetype': 'text/x-python', 'style': 'height: 600px;'})},
    }


# class AppAdmin(admin.ModelAdmin):
#     form = AppAdminForm
# admin.site.register(App, AppAdmin)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'url_part', 'url', 'method')

    readonly_fields = ["url"]

    def has_add_permission(self, request):
        return Service.objects.count() >= 1
