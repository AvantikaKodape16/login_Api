from sqlalchemy import Column, String, Integer,TIMESTAMP, func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class CustomerInfo(Base):
    __tablename__ = 'customer_details'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', String(36))
    mobile = Column('mobile', String(15))
    email = Column('email', String(50), nullable=True, server_default=None)
    otp = Column('otp', String(4), nullable=True)
    is_active = Column('is_active', TINYINT(4), nullable=False, default=1)
    created_on = Column('created_on', TIMESTAMP, nullable=False, default=func.now())
    updated_on = Column('updated_on', TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    deleted_on = Column('deleted_on', TIMESTAMP, nullable=True)



