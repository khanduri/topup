from enum import Enum
from flask import current_app


_app_constants = None


def get_app_constant(key, default):
    global _app_constants
    if not _app_constants:
        load_constants = [
            'CONST_DISABLE_DEBUG_LOGS',

        ]
        _app_constants = {k: int(current_app.config[k] or default) for k in load_constants}
        current_app.logger.info("CONSTANTS_LOADED: {}".format(_app_constants))
    return _app_constants.get(key, default)


class Reason(Enum):
    SIGNIN_FAILED = 'user-signin-failed'
    USER_MISMATCH = 'user-mismatch'
    INVALID = 'invalid-data'
    NOT_SUPPORTED = 'not-supported'
    TOKEN_MISSING = 'token-missing'
    TOKEN_INVALID = 'token-invalid'
    NOT_FOUND = 'not-found'
    INVITE_CODE_INVALID = 'invite-code-invalid'
    INVITE_EMAIL_INVALID = 'invite-email-invalid'
    EXCEPTION = 'exception'
    ORGANIZATION_STOP = 'organization-stop'
    ORGANIZATION_UNSCOPED = 'organization-unscoped'
    ORGANIZATION_NOT_REGISTERED = 'organization-not-registered'
    ORGANIZATION_PILOT_COMPLETE = "organization-pilot-complete"
    USER_PILOT_COMPLETE = "user-pilot-complete"
    ORGANIZATION_NOT_WORK = "ORGANIZATION_NOT_WORK"
    EXPIRED = 'data-expired'
    GHOSTING_FAILED = 'ghosting-failed'

    def message(self, child_message):
        contact_email = ''  # TODO FIX

        parent_message = {
            Reason.USER_MISMATCH: "Sorry! We're unable to process that request for you.",
            Reason.INVALID: 'Invalid operation!',
            Reason.NOT_SUPPORTED: "Sorry! We're unable to process that request for you.",
            Reason.SIGNIN_FAILED: "Something went wrong during the signin process!",
            Reason.TOKEN_MISSING: 'Token is missing!',
            Reason.TOKEN_INVALID: 'Token is invalid!',
            Reason.NOT_FOUND: 'Not Found!',
            Reason.INVITE_CODE_INVALID: 'The invite code or email you entered is invalid!',
            Reason.INVITE_EMAIL_INVALID: 'The email address entered is invalid!',
            Reason.ORGANIZATION_STOP: "Your organization does not have an active account. Please contact us at {}.".format(contact_email),
            Reason.ORGANIZATION_UNSCOPED: "Your organization hasn't been onboarded! Please contact {}.".format(contact_email),
            Reason.ORGANIZATION_NOT_REGISTERED: "Your organization hasn't been onboarded yet! Please contact {} for details.".format(contact_email),
            Reason.ORGANIZATION_PILOT_COMPLETE: "Your organization's pilot period has expired! Please contact {} for details.".format(contact_email),
            Reason.USER_PILOT_COMPLETE: "Your pilot period has expired! Please contact {} or your organization's account admin for details.".format(contact_email),
            Reason.ORGANIZATION_NOT_WORK: "Please use your work email to login!",
            Reason.EXCEPTION: 'An error occurred on our end: Unable to process request at this time!',
            Reason.EXPIRED: 'Data was expired and is not available anymore.',
            Reason.GHOSTING_FAILED: 'Ghosting the user failed!',
        }[self]

        message = parent_message
        if child_message:
            message = "{} - Details: {}".format(message, child_message)

        return message
