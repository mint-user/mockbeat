import json
import re
import pydantic
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.urls.resolvers import RoutePattern
from django.views.decorators.csrf import csrf_exempt
from typing import Tuple
import uuid
from http import HTTPStatus
from json import JSONDecodeError
from strenum import StrEnum
from enum import auto

import requests
from mockbeat.settings import BASE_DIR

from mock_api.models import Endpoint, Strategy

ENDPOINTS = [
    ('/qwe/*', 1),
    ('/rty/*', 2),
]


class Dispatcher:

    @staticmethod
    def get_endpoint_id(path: str) -> str | None:
        for endpoint in Endpoint.objects.values('id', 'url'):
            pattern = RoutePattern(endpoint['url'])
            if pattern.match(path.lstrip('/')) is not None:
                return endpoint['id']
        return None

    @csrf_exempt
    def dispatch(self, request: HttpRequest) -> HttpResponse:
        """Look for handler by path."""

        endpoint_id = self.get_endpoint_id(request.path)

        if endpoint_id is None:
            return HttpResponse(content='Handler not found')

        # VALIDATE DATA TYPE
        if request.headers.get('Content-Type') and request.headers['Content-Type'] == 'application/json':
            try:
                request_body = json.loads(request.body)
            except JSONDecodeError as e:
                return HttpResponse(
                    content=json.dumps({'error': 'Invalid JSON: ' + str(e)}),
                    status=HTTPStatus.BAD_REQUEST,
                )
        else:
            request_body = request.body

        ex_locals = {'request_body': request_body}

        # RUN SCRIPT
        endpoint_logic = Strategy.objects.filter(endpoint_id=endpoint_id)[0].script_body

        exec(endpoint_logic, None, ex_locals)

        # RETURN RESPONSE
        return HttpResponse(
            headers={'Content-Type': 'application/json'},
            content=json.dumps(ex_locals['body']),
            status=ex_locals['http_status'],
        )
