import re

from django.http import HttpRequest, HttpResponse
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from json import JSONDecodeError

import json
import pydantic
from typing import Optional, Tuple
import uuid
from http import HTTPStatus


from mockbeat.settings import BASE_DIR

ENDPOINTS = [
    ('/qwe/*', 1),
    ('/rty/*', 2),
]

endpoint_logic = """
class RequestModel(pydantic.BaseModel):
    amount: str


class ResponseModel(pydantic.BaseModel):
    amount: str
    order_id: str
    status: str


class BaseStrategy:

    def prepare_response(self) -> Tuple[dict, int]:
        raise NotImplemented


class SuccessStrategy(BaseStrategy):

    def prepare_response(self) -> Tuple[dict, int]:
        return ResponseModel(
            amout='123',
            order_id=str(uuid.uuid4()),
            status='success'
        ).dict(), HTTPStatus.OK


request_body = json.loads(request.body)
request_object = RequestModel.parse_obj(request_body)

# SET MARKER
marker = request_object.amount

# CONTEXT

strategy_class = {}.get(marker, SuccessStrategy)

body, http_status = strategy_class().prepare_response()
 """


@csrf_exempt
def dispatcher(request: HttpRequest) -> HttpResponse:
    """Look for handler by path."""

    for endpoint in ENDPOINTS:
        endpoint_path_pattern = endpoint[0]
        if re.match(pattern=endpoint_path_pattern, string=request.path):
            ex_locals = {'request': request}

            with open(f'{BASE_DIR}/mock_api/views.py') as f:
                endpoint_logic = f.read()
                print(endpoint_logic)
                exec(endpoint_logic, None, ex_locals)
                print(ex_locals['body'])
                print(ex_locals['http_status'])
                return HttpResponse(
                    headers={'Content-Type': 'application/json'},
                    content=json.dumps(ex_locals['body']),
                    status=ex_locals['http_status'],
                )

    return HttpResponse(content='Handler not found')


urlpatterns = [
    re_path(r'.*', dispatcher),
]
