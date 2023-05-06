import uuid
from http import HTTPStatus
from json import JSONDecodeError

import pydantic
import json
from typing import Tuple

import requests


def handle_request(request: requests.Request) -> Tuple[dict | str, int]:
    # VALIDATE DATA TYPE
    if request.headers.get('Content-Type') and request.headers['Content-Type'] == 'application/json':
        try:
            request_body = json.loads(request.body)
        except JSONDecodeError as e:
            return {'error': 'Invalid JSON: ' + str(e)}, HTTPStatus.BAD_REQUEST

    else:
        request_body = request.body

    # PARSE REQUEST
    class RequestModel(pydantic.BaseModel):
        amount: str

    request_object = RequestModel.parse_obj(request_body)

    # SET MARKER
    marker = request_object.amount

    # STRATEGIES
    class BaseStrategy:
        status: str

        def prepare_response(self, request_object: 'RequestModel') -> Tuple[dict, int]:
            raise NotImplemented

    class SuccessStrategy(BaseStrategy):
        status = 'success'

        def prepare_response(self, request_object: 'RequestModel') -> Tuple[dict, int]:
            return {
                'amount': request_object.amount,
                'order_id': str(uuid.uuid4()),
                'status': self.status,
            }, HTTPStatus.OK

    class FailedStrategy(SuccessStrategy):
        status = 'failed'

    # CONTEXT
    strategy_class = {
        '1': SuccessStrategy,
        '2': FailedStrategy,
    }.get(marker, SuccessStrategy)

    return strategy_class().prepare_response(request_object)


body, http_status = handle_request(request)
