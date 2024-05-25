from sqlalchemy.orm import Session
from datetime import datetime
import random

from backend.database.models import (
    Categoria, Producto, PrecioProducto)


def crear_categorias_y_productos(db: Session):
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
                cat_obj = Categoria(name=subcategoria)
                db.add(cat_obj)
                db.commit()
                crear_productos(db, cat_obj, productos, marcas)
        else:
            cat_obj = Categoria(name=categoria_principal)
            db.add(cat_obj)
            db.commit()
            crear_productos(db, cat_obj, subcategorias, marcas)


def crear_productos(db: Session, categoria, productos, marcas):
    for producto in productos:
        for _ in range(3):
            codigo_producto = f'{producto[:3].upper()}-{random.randint(100, 999)}'
            prod_obj = Producto(
                codigo_producto=codigo_producto,
                marca=random.choice(marcas),
                codigo=f'{producto[:3].upper()}-{random.randint(1000, 9999)}',
                name=producto,
                cat=categoria,
                stock=random.randint(1, 100)
            )
            db.add(prod_obj)
            db.commit()
            precio_prod = PrecioProducto(
                producto=prod_obj,
                valor=random.randint(1, 100)
            )
            db.add(precio_prod)
            db.commit()
