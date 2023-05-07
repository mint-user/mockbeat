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
        self.url = urljoin(f'{self.service.base_url}/', self.url_part)  # noqa
        super(Endpoint, self).save(*args, **kwargs)

    def create(self, name: str, service: Service, url_part: str, method: HTTPMethod) -> None:

        Endpoint(
            name=name,
            service=service,
            url_part=url_part,
            method=method.value,
            url=urljoin(f'{service.base_url}/', url_part),
        ).save()


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

