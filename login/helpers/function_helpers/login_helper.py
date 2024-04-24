import random
import jwt
import uuid
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status

from login.helpers.query_helpers.login_helper import (
    get_customer_by_mobile,
    create_customer,
    update_customer_otp
)
from login.common import messages as glob_messages


def generate_otp(length=4):
    """Generate a random OTP of specified length."""
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp

def create_customer_with_otp(request):
    mobile = str(request.data.get('mobile'))
    mobile_customer = get_customer_by_mobile(mobile=mobile)
    
    if not mobile_customer:
        otp = str(generate_otp())
        uuid4_code = str(uuid.uuid4())
        
        add_data = {
            'code' : uuid4_code,
            'mobile' : mobile,
            'otp' : otp
        }
        add_customer = create_customer(add_data)
        customer_id = add_customer.get('customer_id')

        if add_customer:
            return Response({
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'OTP sent successfully',
                'data': {
                    'customer_id': customer_id,
                    'mobile':mobile,
                    'otp': otp
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'There was a problem while sending OTP',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    elif mobile_customer:
        customer_id = mobile_customer.get('customer_id')
        otp = generate_otp()
        update_customer = update_customer_otp(mobile, otp)

        if update_customer:
            return Response({
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'OTP sent successfully',
                'data': {
                    'customer_id': customer_id,
                    'mobile':mobile,
                    'otp': otp
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'There was a problem while sending OTP',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

def verify_otp(request):
    mobile = request.data.get('mobile')
    otp = request.data.get('otp')
    
    customer = get_customer_by_mobile(mobile)
    if customer.get('otp') == otp:  
        user_id = customer.get('user_id')    
        access_token = generate_access_token(user_id)
        if access_token:
            return Response({
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': glob_messages.LOGIN_SUCCESSFUL,
                'data': {
                    'access_token': access_token
                }
            }, status=status.HTTP_200_OK)
        else :
            return Response({
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': glob_messages.LOGIN_SUCCESSFUL,
                'data': {

                }
            }, status=status.HTTP_200_OK)
    else: 
        return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': glob_messages.LOGIN_FAILED,
                    'data': {
                      
                        }
                }, status=status.HTTP_400_BAD_REQUEST)  
        
def generate_access_token(user_id):
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=15),  # Token expiration time
            'iat': datetime.utcnow()  # Token issue time
        }
        access_token = jwt.encode(payload, "#tsey-(vnsilc75x*l97m03ehas3m5_b2!tv0rs1ghkox1#%f+", algorithm='HS256')
        print("access_token",access_token)
        return access_token
    except Exception as e:
        print("An error occurred while generating access token:", e)
        return None
    

# def generate_refresh_token(user_id):
#     try:
#         payload = {
#             'user_id': user_id,
#             'exp': datetime.utcnow() + timedelta(days=30),  # Refresh token expiration time
#             'iat': datetime.utcnow()  # Refresh token issue time
#         }
#         refresh_token = jwt.encode(payload, settings.REFRESH_TOKEN_SECRET_KEY, algorithm='HS256')
#         return refresh_token
#     except Exception as e:
#         print("An error occurred while generating refresh token:", e)
#         return None
