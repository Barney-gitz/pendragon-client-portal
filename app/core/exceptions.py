class AuthenticationError(Exception):
    """Base class for authentication-related exceptions."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised when attempting to create a user that already exists."""


class PasswordMismatchError(AuthenticationError):
    """Raised when the supplied passwords do not match."""


class InvalidInvitationError(AuthenticationError):
    """Raised when an invitation token cannot be found."""


class InvitationExpiredError(AuthenticationError):
    """Raised when an invitation has expired."""


class InvitationAlreadyAcceptedError(AuthenticationError):
    """Raised when an invitation has already been accepted."""


class InvitationInvalidatedError(AuthenticationError):
    """Raised when an invitation has been superseded."""