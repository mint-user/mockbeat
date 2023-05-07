import re

from django.http import HttpRequest, HttpResponse
from django.urls import re_path, path
from django.views.decorators.csrf import csrf_exempt
from json import JSONDecodeError

import json
import pydantic
from typing import Optional, Tuple
import uuid
from http import HTTPStatus


from mockbeat.settings import BASE_DIR

from mock_api import views

ENDPOINTS = [
    ('/qwe/*', 1),
    ('/rty/*', 2),
]


@csrf_exempt
def dispatcher(request: HttpRequest) -> HttpResponse:
    """Look for handler by path."""

    for endpoint in ENDPOINTS:
        endpoint_path_pattern = endpoint[0]
        if re.match(pattern=endpoint_path_pattern, string=request.path):
            ex_locals = {'request': request}

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

    return HttpResponse(content='Handler not found')


urlpatterns = [
    re_path(r'.*', dispatcher),
]
