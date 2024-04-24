
from login.common import constants as glob_constants

CREATE_CUSTOMER =  {
    'mobile': {
        'required': True,
        'empty': False,
        'type': 'string'
    }

}

VERIFY_OTP = {
    'mobile': {
            'required': True,
            'empty': False,
            'type': 'string'
    },
    'otp': {
            'required': True,
            'empty': True,
            'type': 'string'
        }
}