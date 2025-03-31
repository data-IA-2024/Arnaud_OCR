from sqlalchemy import Column, String, Numeric, ForeignKey, Date, MetaData
from sqlalchemy.orm import declarative_base, relationship
import os

Base = declarative_base(metadata=MetaData(schema=os.environ.get('DB_SCHM')))

class Customer(Base):
    __tablename__ = 'customers'
    
    email = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False) 
    gender = Column(String, nullable=True)
    adress = Column(String, nullable=True)
    birth = Column(Date, nullable=True)

    invoices = relationship("Invoice", back_populates="customer")

    def __repr__(self):
        return f"Customer {self.email} | Gender: {self.gender} | Birth: {self.birth}"

class Invoice(Base):
    __tablename__ = 'invoices'
    
    invoice_number = Column(String, primary_key=True, nullable=False)
    total = Column(Numeric(8,2))
    customer_email = Column(String, ForeignKey('customers.email'), nullable=False)
    creation_date = Column(Date, nullable=False)

    customer = relationship("Customer", back_populates="invoices")

    def __repr__(self):
        return f"Invoice {self.invoice_number} | Customer: {self.customer_email} | Date: {self.creation_date}"
