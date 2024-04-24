import re
import json
from cerberus import Validator
import datetime

from login.common import messages as glob_messages


from login.common import constants as product_constants


class CustomValidator(Validator):


    # Validate Numeric
    def _validate_isnumeric(self, isnumeric, field, value):
        """
        {'type':'boolean'}
        """
        if isnumeric:
            try:
                number = int(value)
            except Exception:
                self._error(field, glob_messages.INTEGER_ONLY)


    # Validate Alpha Numeric
    def _validate_isalphanumeric(self, isalphanumeric, field, value):
        """
        {'type':'boolean'}
        """
        if isalphanumeric:
            zeroes = re.match('^0+$', value)
            if zeroes:
                self._error(
                    field, glob_messages.INVALID_ALPHANUMERIC)

            alphanumeric_id = re.match('^(?![0-9_ -]*$)[a-zA-Z0-9_ -]+$', value)

            if not alphanumeric_id:
                self._error(
                    field, glob_messages.INVALID_ALPHANUMERIC)


    # Validate Email
    def _validate_isemail(self, isemail, field, value):
        """
            {'type': 'boolean'}
         """

        if isemail:
            email = re.match(
                '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                value
            )

            if not email:
                self._error(field, glob_messages.INVALID_EMAIL)


        # Validate Mobile
    def _validate_ismobile(self,ismobile,field,value):
        """
        {'type':'boolean'}
        """
        if ismobile:
            mobile = re.match('^[6-9]\d{9}$', value)
            if (not mobile or
                not len(value) == 10
            ):
                self._error(field,glob_messages.INVALID_MOBILE_NUMBER)