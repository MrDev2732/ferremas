from sqlalchemy.orm import Session
from datetime import datetime
import random

from backend.database.models import Producto, Categoria


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
                crear_categoria(session, subcategoria)
                crear_productos(session, subcategoria, productos, marcas)
        else:
            crear_categoria(session, categoria_principal)
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


def crear_categoria(session: Session, name: str, desc: str = None):
    # Buscar si ya existe una categoría con el mismo nombre
    instance = session.query(Categoria).filter_by(name=name).first()
    if instance:
        return instance
    else:
        # Crear una nueva instancia de Categoria si no existe
        now = datetime.now()
        nueva_categoria = Categoria(
            name=name,
            desc=desc,
            enabled=True,  # Valor predeterminado definido en el modelo
            created_date=now,
            modified_date=now,
            deleted_date=None  # Puede ser NULL según el modelo
        )
        session.add(nueva_categoria)
        session.commit()
        return nueva_categoria
