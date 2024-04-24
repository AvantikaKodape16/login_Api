# app url here
from django.urls import path
from login.apiviews.login import MobileOTPLoginView, VerifyOTP 

urlpatterns = [
   path('check-mobile', MobileOTPLoginView.as_view(), name='check-mobile'),
  
  path('verify', VerifyOTP.as_view(), name='verify'),
]
