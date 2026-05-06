class ServiceException(Exception):
    pass


class InvalidFileException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundException(ServiceException):
    def __init__(
        self,
        resource: str,
        identifier: str,
        object: str | None = None,
    ):
        if object:
            msg = f"object {object} of {resource} not found: {identifier}"
        else:
            msg = f"{resource} not found: {identifier}"

        super().__init__(msg)
        self.resource = resource
        self.identifier = identifier
        self.object = object


class ConflictException(ServiceException):
    def __init__(
        self,
        resource: str,
        identifier: str,
        object: str,
    ):
        msg = f"object {object} of {resource} already exists: {identifier}"

        super().__init__(msg)
        self.resource = resource
        self.identifier = identifier
        self.object = object

class ForbiddenException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
