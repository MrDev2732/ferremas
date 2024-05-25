from sqlalchemy.orm import Session
from datetime import datetime
import random

from backend.database.models import Producto


def crear_categorias_y_productos(session: Session):
    categorias = {
        'Herramientas': {
            'Herramientas Manuales': ['Martillos', 'Destornilladores', 'Llaves'],
            'Herramientas Eléctricas': ['Taladros', 'Sierras', 'Lijadoras']
        },
        'Materiales de Construcción': {
            'Materiales Básicos': ['Cemento', 'Arena', 'Ladrillos'],
            'Acabados': ['Pinturas', 'Barnices', 'Cerámicos']
        },
        'Equipos de Seguridad': ['Casos', 'Guantes', 'Lentes de Seguridad'],
        'Accesorios Varios': ['Tornillos y Anclajes', 'Fijaciones y Adhesivos', 'Equipos de Medición']
    }

    marcas = ['Bosch', 'Makita', 'Stanley', '3M', 'Samsung']

    for categoria_principal, subcategorias in categorias.items():
        if isinstance(subcategorias, dict):
            for subcategoria, productos in subcategorias.items():
                crear_productos(session, subcategoria, productos, marcas)
        else:
            crear_productos(session, categoria_principal, subcategorias, marcas)


def crear_productos(session: Session, categoria, productos, marcas):
    for producto in productos:
        codigo_producto = f'{producto[:3].upper()}-{random.randint(100, 999)}'
        now = datetime.now()
        precios = [
            {
                "fecha": now.isoformat(),
                "valor": random.randint(1, 100)
            }
        ]
        prod_obj = Producto(
            id=codigo_producto,
            marca=random.choice(marcas),
            name=producto,
            categoria=categoria,
            stock=random.randint(1, 100),
            imagen=None,
            enabled=True,
            created_date=now,
            modified_date=now,
            deleted_date=None,
            precios=precios
        )
        session.add(prod_obj)
    session.commit()


def get_or_create(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        # Asegurarse de que todos los campos NOT NULL tengan un valor predeterminado
        now = datetime.now()
        defaults = {
            'enabled': True,
            'created_date': now,
            'modified_date': now,
            'deleted_date': None  # Asumiendo que puede ser NULL
        }
        # Actualizar los valores predeterminados con cualquier valor proporcionado en kwargs
        defaults.update(kwargs)
        instance = model(**defaults)
        session.add(instance)
        session.commit()
        return instance
