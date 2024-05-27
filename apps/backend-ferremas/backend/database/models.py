from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import LargeBinary, Column, Integer, String, DateTime, Boolean, JSON
from datetime import datetime


Base = declarative_base()


class BaseModel:
    enabled = Column(Boolean, default=True)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    deleted_date = Column(DateTime, nullable=True)


class Categoria(Base, BaseModel):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True)
    desc = Column(String(500), nullable=True)


class Producto(Base, BaseModel):
    __tablename__ = 'producto'

    id = Column(String(20), primary_key=True)
    marca = Column(String(50))
    name = Column(String(150))
    categoria = Column(String)
    stock = Column(Integer, default=0)
    imagen = Column(LargeBinary, nullable=True)
    precios = Column(JSON, nullable=False)  # Campo JSON para almacenar precios


    def add_precio(self, valor, fecha=None):
        if fecha is None:
            fecha = datetime.now().isoformat()
        if self.precios is None:
            self.precios = []
        self.precios.append({'valor': valor, 'fecha': fecha})
        # No convertir a JSON aquí, manejar como lista de Python


    def get_precios(self):
        if self.precios:
            return self.precios  # Asumiendo que self.precios ya está en el formato correcto
        return []

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(150), nullable=False)
    nombre = Column(String(150), unique=True, nullable=False)
    rol = Column(String(150), nullable=False)


