import json
import re
import pydantic
from django.http import HttpRequest, HttpResponse
from django.urls.resolvers import RoutePattern
from django.views.decorators.csrf import csrf_exempt
from typing import Tuple
import uuid
from http import HTTPStatus
from json import JSONDecodeError

import requests
from mockbeat.settings import BASE_DIR

from mock_api.models import Endpoint

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

        with open(f'{BASE_DIR}/mock_api/script.py') as f:
            endpoint_logic = f.read()
            # print(endpoint_logic)
            exec(endpoint_logic, None, ex_locals)
            # print(ex_locals['body'])
            # print(ex_locals['http_status'])
            return HttpResponse(
                headers={'Content-Type': 'application/json'},
                content=json.dumps(ex_locals['body']),
                status=ex_locals['http_status'],
            )

