from app.requests.user_list import UserListInvalidRequest
from app.responses import ResponseSuccess, build_response_from_invalid_request, ResponseTypes, ResponseFailure

SUCCESS_VALUE = {"key": ["value1", "value2"]}
GENERIC_RESPONSE_TYPE = "Response"
GENERIC_RESPONSE_MESSAGE = 'This is a response'


def test_response_success_is_true():
    response = ResponseSuccess(SUCCESS_VALUE)
    assert bool(response) is True


def test_response_failure_is_false():
    response = ResponseFailure(GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE)
    assert bool(response) is False


def test_response_success_has_type_and_value():
    response = ResponseSuccess(SUCCESS_VALUE)

    assert response.type == ResponseTypes.SUCCESS
    assert response.value == SUCCESS_VALUE


def test_response_failure_has_type_and_mesage():
    response = ResponseFailure(GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE)

    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.value == {
        "type": GENERIC_RESPONSE_TYPE,
        "message": GENERIC_RESPONSE_MESSAGE
    }


def test_response_failure_initialization_with_exception():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE,
        Exception('Just an error message')
    )

    assert bool(response) is False
    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == 'Exception: Just an error message'


def test_response_failure_from_empty_invalid_request():
    response = build_response_from_invalid_request(
        UserListInvalidRequest()
    )

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_with_errors():
    request = UserListInvalidRequest()
    request.add_error('path', 'is mandatory')
    request.add_error('path', 'cannot be blank')

    response = build_response_from_invalid_request(request)

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR
    assert response.message == "path: is mandatory\npath: cannot be blank"
