from sqlalchemy.orm import Session
import hashlib
from datetime import datetime

from backend.database.models import User


def create_user_db(session: Session, password, name, rol):
    # Crear el objeto userabout:blank#blocked
    user = User(
        password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
        name=name,
        rol=rol,
    )
    # Agregar el user a la sesión y confirmar los cambios
    session.add(user)
    session.commit()
    return user


def update_product_db(session: Session, user_id: str, user: dict):
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.items():
            if hasattr(db_user, key) and getattr(db_user, key) != value:
                if value is not None:
                    setattr(db_user, key, value)
        db_user.modified_date = datetime.now()
        session.commit()
        return db_user
    return None


def delete_product_db(session: Session, user_id: str):
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user:
        session.delete(db_user)
        session.commit()
        return True
    return False
