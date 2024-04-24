import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from login.common import messages as glob_messages
from rest_framework.versioning import NamespaceVersioning
from login.validations  import schemas
from rest_framework.permissions import AllowAny
from login.utils import custom_exceptions as ce
from login.utils.custom_validation import CustomValidator

from login.helpers.function_helpers.login_helper import create_customer_with_otp, verify_otp

logger = logging.getLogger(__name__)

c_validator = CustomValidator({}, allow_unknown=True)

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class MobileOTPLoginView(APIView):
    versioning_class = VersioningConfig
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
    
        if request.version == 'v1':
            schema = schemas.CREATE_CUSTOMER

            is_valid = c_validator.validate(request.data, schema)

            if is_valid:
                    result = create_customer_with_otp(request)
                    return result
            else:
                raise ce.ValidationFailed({
                    'message': glob_messages.VALIDATION_FAILED,
                    'data': c_validator.errors
                })

        else:
            raise ce.VersionNotSupported


class VerifyOTP(APIView):

    versioning_class = VersioningConfig
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        try:
            if request.version == 'v1':
                schema = schemas.VERIFY_OTP

                is_valid = c_validator.validate(request.data, schema)
                if not is_valid:
                    raise ce.ValidationFailed({
                        'message': glob_messages.VALIDATION_FAILED,
                        'data': c_validator.errors
                    })

                result = verify_otp(request)

                return result

            else:
                raise ce.VersionNotSupported

        except ce.ValidationFailed as vf:
            raise

