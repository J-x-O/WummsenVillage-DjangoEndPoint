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


def extract_json(request: Request):
    try:
        return json.loads(request.body)
    except JSONDecodeError:
        raise ExpectedJSONException()


# --- Single Params ----------------------------------------------------------------------------------------------------


def extract_optional_param(request: Request, key: str, default: any):
    return extract_json(request).get(key, default)


def validate_required_param(request: Request, required_param: str):
    return validate_json_param(extract_json(request), required_param)


def validate_json_param(data: dict, required_param: str):
    if required_param not in data:
        raise MissingParametersException()

    return data[required_param]


# --- Multiple Params --------------------------------------------------------------------------------------------------


def extract_optional_json_params(data: dict, optional_params: dict[str, any]):
    return tuple(data.get(param, optional_params[param]) for param in optional_params)


def extract_optional_params(request: Request, optional_params: dict[str, any]):
    return extract_optional_json_params(extract_json(request), optional_params)


def validate_required_params(request: Request, required_params: list[str]):
    return validate_json_params(extract_json(request), required_params)


def validate_json_params(data: dict, required_params: list[str]):
    if not all(param in data for param in required_params):
        # some or all of the required parameters are missing
        raise MissingParametersException()
    return tuple(data[param] for param in required_params)
