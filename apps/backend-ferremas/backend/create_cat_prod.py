from sqlalchemy.orm import Session
from datetime import datetime
import random

from backend.database.models import Product, Category


def create_category_and_product(session: Session):
    category = {
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

    brand = ['Bosch', 'Makita', 'Stanley', '3M', 'Samsung']

    for main_category, subcategory in category.items():
        if isinstance(subcategory, dict):
            for subcategoria, productos in subcategory.items():
                create_category(session, subcategoria)
                create_product(session, subcategoria, productos, brand)
        else:
            create_category(session, main_category)
            create_product(session, main_category, subcategory, brand)

def create_product(session: Session, category, product, brand):
    for product in product:
        code_product = f'{product[:3].upper()}-{random.randint(100, 999)}'
        now = datetime.now()
        price = [
            {
                "date": now.isoformat(),
                "price": random.randint(1, 100)
            }
        ]
        prod_obj = Product(
            id=code_product,
            brand=random.choice(brand),
            name=product,
            category=category,
            stock=random.randint(1, 100),
            image=None,
            enabled=True,
            created_date=now,
            modified_date=now,
            deleted_date=None,
            price=price
        )
        session.add(prod_obj)
    session.commit()


def create_category(session: Session, name: str, desc: str = None):
    # Buscar si ya existe una categoría con el mismo nombre
    instance = session.query(Category).filter_by(name=name).first()
    if instance:
        return instance
    else:
        # Crear una nueva instancia de Category si no existe
        now = datetime.now()
        new_category = Category(
            name=name,
            desc=desc,
            enabled=True,  # Valor predeterminado definido en el modelo
            created_date=now,
            modified_date=now,
            deleted_date=None  # Puede ser NULL según el modelo
        )
        session.add(new_category)
        session.commit()
        return new_category
