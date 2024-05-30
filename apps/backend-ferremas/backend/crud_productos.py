import random
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.database.models import Product


def create_product_db(session: Session, category, product, brand, image = None):
    code_product = f'{product[:3].upper()}-{random.randint(100, 999)}'
    now = datetime.now()
    price = [
            {
                "date": now.isoformat(),
                "price": random.randint(1, 100)
            }
        ]
    db_product = Product(
            id=code_product,
            brand=brand,
            name=product,
            category=category,
            stock=random.randint(1, 100),
            image= image,
            enabled=True,
            created_date=now,
            modified_date=now,
            deleted_date=None,
            price=price
        )
    session.add(db_product)
    session.commit()
    return db_product

def convert_image_to_binary(image: UploadFile):
    return image.read()


def update_product_db(session: Session, product_id: str, product: dict):
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.items():
            if hasattr(db_product, key) and getattr(db_product, key) != value:
                if value is not None:
                    setattr(db_product, key, value)
        db_product.modified_date = datetime.now()
        session.commit()
        return db_product
    return None


def delete_product_db(session: Session, product_id: str):
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if db_product:
        session.delete(db_product)
        session.commit()
        return True
    return False
