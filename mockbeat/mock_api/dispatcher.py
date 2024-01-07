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

from mock_api.enums import HTTPMethod
from mock_api.models import Endpoint, Strategy


class Dispatcher:

    @staticmethod
    def get_endpoint_id(request: HttpRequest) -> str | None:
        for endpoint in Endpoint.objects.values('id', 'url').filter(method=request.method):
            pattern = RoutePattern(endpoint['url'])
            if pattern.match(request.path.lstrip('/')) is not None:
                return endpoint['id']
        return None

    @csrf_exempt
    def dispatch(self, request: HttpRequest) -> HttpResponse:
        """Look for handler by path."""

        endpoint_id = self.get_endpoint_id(request)

        if endpoint_id is None:
            return HttpResponse(content='Handler not found', status=HTTPStatus.NOT_FOUND)

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

        full_script = ('def handle_request(request_body: dict | str) -> Tuple[dict | str, int]:\n' +
                       endpoint_logic + '\nbody, http_status = handle_request(request_body)')

        exec(full_script, None, ex_locals)

        # RETURN RESPONSE
        return HttpResponse(
            headers={'Content-Type': 'application/json'},
            content=json.dumps(ex_locals['body']),
            status=ex_locals['http_status'],
        )
