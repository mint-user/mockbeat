import uuid
from http import HTTPStatus

import pydantic
from typing import Tuple


def handle_request(request_body: dict | str) -> Tuple[dict | str, int]:
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


body, http_status = handle_request(request_body)
