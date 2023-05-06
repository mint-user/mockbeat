from http import HTTPMethod

from django.db import models


class Service(models.Model):

    class Meta:
        db_table = 'services'

    name = models.CharField(unique=True, null=False, max_length=255)
    base_url = models.CharField(unique=True, null=False, max_length=100)


class Endpoint(models.Model):

    class Meta:
        db_table = 'endpoints'

    METHODS = (
        ('available', _('Available to borrow')),
        ('borrowed', _('Borrowed by someone')),
        ('archived', _('Archived - not available anymore')),
    )

    name = models.CharField(unique=True, null=False, max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    url_part = models.CharField(unique=True, null=False, max_length=100, default='')
    url = models.CharField(unique=True, null=False, max_length=100)
    method = models.CharField(null=False, choices=HTTPMethod)


class Context(models.Model):

    class Meta:
        db_table = 'contexts'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script = models.TextField


class Schema(models.Model):

    class Meta:
        db_table = 'schemas'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script = models.TextField


class Strategy(models.Model):

    class Meta:
        db_table = 'strategies'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script = models.TextField


class Marker(models.Model):

    class Meta:
        db_table = 'markers'

    name = models.CharField(unique=True, null=False, max_length=255)
    schema_id = models.ForeignKey(Schema, on_delete=models.CASCADE)
    script = models.TextField
