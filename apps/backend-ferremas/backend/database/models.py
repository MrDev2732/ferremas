from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, LargeBinary
from datetime import datetime


Base = declarative_base()


class BaseModel:
    enabled = Column(Boolean, default=True)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    deleted_date = Column(DateTime, nullable=True)


class Category(Base, BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True)
    desc = Column(String(500), nullable=True)


class Transactions(Base, BaseModel):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    payer_id = Column(String(150), nullable=False)
    transaction_id = Column(String(150), unique=True, nullable=False)
    payment_status = Column(String(50), nullable=False)
    payment_method = Column(String(50), default='PayPal')
    description = Column(String(500), nullable=True)


class Product(Base, BaseModel):
    __tablename__ = 'product'

    id = Column(String(20), primary_key=True)
    brand = Column(String(50))
    name = Column(String(150))
    category = Column(String)
    stock = Column(Integer, default=0)
    image = Column(LargeBinary, nullable=True)
    price = Column(JSON, nullable=False)


    def add_price(self, price, date=None):
        if date is None:
            date = datetime.now().isoformat()
        if self.price is None:
            self.price = []
        self.price.append({'price': price, 'date': date})


    def get_price(self):
        if self.price:
            return self.price 
        return []


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    rol = Column(String(150), nullable=False)
