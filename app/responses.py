class ResponseTypes:
    """
    The error types contained in the ResponseTypes class are very similar to HTTP errors. This similarity will be
    useful when we return responses from the web framework.

    PARAMETERS_ERROR signals that something was wrong in the input parameters passed by the request.

    RESOURCE_ERROR signals that the process ended correctly, but the requested resource isn’t available. Lastly,

    SYSTEM_ERROR signals that something went wrong with the process itself. These are used mostly to signal an
    exception in the Python code.
    """
    PARAMETERS_ERROR = 'ParametersError'
    RESOURCE_ERROR = 'ResourceError'
    SYSTEM_ERROR = 'SystemError',
    SUCCESS = 'Success'


class ResponseFailure:
    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @property
    def value(self):
        return {"type": self.type, "message": self.message}

    def __bool__(self):
        return False


class ResponseSuccess:
    def __init__(self, value=None):
        self.type = ResponseTypes.SUCCESS
        self.value = value

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    message = "\n".join(
        [
            "{}: {}".format(err["parameter"], err["message"])
            for err in invalid_request.errors
        ]
    )
    return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, message)