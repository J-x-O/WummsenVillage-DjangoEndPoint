import json
from json import JSONDecodeError

from rest_framework.exceptions import APIException
from rest_framework.request import Request


class MissingParametersException(APIException):
    status_code = 400
    default_detail = 'Not all required Parameters where provided'
    default_code = 'bad_request'


class ExpectedJSONException(APIException):
    status_code = 400
    default_detail = 'Please provide valid Json-Data'
    default_code = 'bad_request'


def validate_json_params(data: any, required_params: list[str]):
    if not all(param in data for param in required_params):
        # some or all of the required parameters are missing
        raise MissingParametersException()
    return tuple(data[param] for param in required_params)


def validate_required_params(request: Request, required_params: list[str]):
    try:
        return validate_json_params(extract_json(request), required_params)
    except MissingParametersException and ExpectedJSONException:
        return validate_json_params(request.query_params, required_params)


def validate_json_param(data: any, required_param: str):
    if required_param not in data:
        raise MissingParametersException()

    return data[required_param]


def validate_required_param(request: Request, required_param: str):
    try:
        return validate_json_param(extract_json(request), required_param)
    except MissingParametersException:
        return validate_json_param(request.query_params, required_param)


def extract_json(request: Request):
    try:
        return json.loads(request.body)
    except JSONDecodeError:
        raise ExpectedJSONException()
