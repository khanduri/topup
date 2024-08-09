import enum
from collections import namedtuple

TOPUP_FEES = 1
MAX_ACTIVE_BENEFICIARIES = 5
MAX_MONTHLY_LIMIT = 3000
MAX_BENEFICIARY_VERIFIED_LIMIT = 1000
MAX_BENEFICIARY_UNVERIFIED_LIMIT = 500


Action = namedtuple('Action', 'name')


class ActionEnum(enum.Enum):
    BALANCE_ADD = Action('balance_add')
    VERIFY_USER = Action('verify_user')
    BENEFICIARY_CREDIT = Action('beneficiary_credit')
    BENEFICIARY_ACTIVATE = Action('beneficiary_activate')
    BENEFICIARY_DEACTIVATE = Action('beneficiary_deactivate')
