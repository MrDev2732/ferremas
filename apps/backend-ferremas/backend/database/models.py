from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import LargeBinary, Column, Integer, String, DateTime, Boolean, JSON
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


class Product(Base, BaseModel):
    __tablename__ = 'product'

    id = Column(String(20), primary_key=True)
    brand = Column(String(50))
    name = Column(String(150))
    category = Column(String)
    stock = Column(Integer, default=0)
    image = Column(LargeBinary, nullable=True)
    price = Column(JSON, nullable=False)  # Campo JSON para almacenar price


    def add_price(self, price, date=None):
        if date is None:
            date = datetime.now().isoformat()
        if self.price is None:
            self.price = []
        self.price.append({'price': price, 'date': date})
        # No convertir a JSON aquí, manejar como lista de Python


    def get_price(self):
        if self.price:
            return self.price  # Asumiendo que self.price ya está en el formato correcto
        return []

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(150), nullable=False)
    name = Column(String(150), unique=True, nullable=False)
    rol = Column(String(150), nullable=False)


