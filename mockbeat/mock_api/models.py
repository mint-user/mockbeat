from urllib.parse import urljoin

from django.db import models

from .enums import HTTPMethod


class Service(models.Model):

    class Meta:
        db_table = 'services'

    name = models.CharField(unique=True, null=False, max_length=255)
    base_url = models.CharField(unique=True, null=False, max_length=100)

    def __str__(self):
        return f'{self.name}'


class Endpoint(models.Model):

    class Meta:
        db_table = 'endpoints'

    class HTTPMethod(models.TextChoices):
        CONNECT = 'CONNECT'
        DELETE = 'DELETE'
        GET = 'GET'
        HEAD = 'HEAD'
        OPTIONS = 'OPTIONS'
        PATCH = 'PATCH'
        POST = 'POST'
        PUT = 'PUT'
        TRACE = 'TRACE'

    name = models.CharField(unique=True, null=False, max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    url_part = models.CharField(unique=False, null=False, max_length=100, default='')
    url = models.CharField(unique=True, null=False, max_length=100)
    method = models.CharField(null=False, choices=HTTPMethod.choices, max_length=10)

    # Override the update function to modify the Post data
    def save(self, *args, **kwargs) -> None:
        """Generate full URL to endpoint."""
        stripped_base_url = self.service.base_url.strip('/')
        stripped_url_part = self.url_part.strip('/')
        self.url = urljoin(f'{stripped_base_url}/', f'{stripped_url_part}/')
        # self.url = urljoin(f'{self.service.base_url}/', self.url_part)  # noqa
        super(Endpoint, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.service} - {self.name}'


class Context(models.Model):

    class Meta:
        db_table = 'contexts'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script = models.TextField(blank=True)


class Schema(models.Model):

    class Meta:
        db_table = 'schemas'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script = models.TextField(blank=True)


class Strategy(models.Model):

    class Meta:
        db_table = 'strategies'

    name = models.CharField(unique=True, null=False, max_length=255)
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    script_body = models.TextField(blank=True)


class Marker(models.Model):

    class Meta:
        db_table = 'markers'

    name = models.CharField(unique=True, null=False, max_length=255)
    schema_id = models.ForeignKey(Schema, on_delete=models.CASCADE)
    script = models.TextField(blank=True)

