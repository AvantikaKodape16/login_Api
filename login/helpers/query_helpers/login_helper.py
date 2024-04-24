from login.models import CustomerInfo
from django.conf import settings

session = settings.DB_SESSION

def result_row(row):
    return row._asdict()

def get_customer_by_mobile(mobile):
    try:
        customer = session.query(
            CustomerInfo.id, CustomerInfo.otp
            ).filter(
                CustomerInfo.mobile == mobile,
                CustomerInfo.deleted_on.is_(None),
                CustomerInfo.is_active == 1
            ).one_or_none()
        
        if customer:
            customer = result_row(customer)

    except Exception as e:
        customer = None
        print(f'get customer details - {e}')
    
    return customer

def create_customer(add_data = None):
    try:
        # Create a new CustomerInfo object with the provided mobile and otp
        new_customer = CustomerInfo(
            **add_data
        )
        
        session.add(new_customer)
        session.commit()

        data = {
            'customer_id' : new_customer.id
        }
        
    except Exception as e:
        data = None
        print("An error occurred while creating a customer:", e)
    
    return data

def update_customer_otp(mobile: str, otp: str,):
    try:
        # Update the customer's OTP with the new value
        customer = session.query(CustomerInfo
                                 ).filter(CustomerInfo.mobile == mobile)
        
        #customer.otp = new_otp
        if customer:
            customer.update({'otp':otp})
        session.commit()
        
        return customer
    except Exception as e:
       
        print("An error occurred while updating customer OTP:", e)
        return None
    

