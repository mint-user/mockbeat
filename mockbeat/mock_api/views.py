import uuid
from http import HTTPStatus

import pydantic
import json
from typing import Tuple


class RequestModel(pydantic.BaseModel):
    amount: str


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


# PARSE REQUEST
request_body = json.loads(request.body)
request_object = RequestModel.parse_obj(request_body)

# SET MARKER
marker = request_object.amount

# CONTEXT
strategy_class = {
    '1': SuccessStrategy,
    '2': FailedStrategy,
}.get(marker, SuccessStrategy)

body, http_status = strategy_class().prepare_response(request_object)


