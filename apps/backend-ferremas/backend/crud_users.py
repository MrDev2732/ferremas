from sqlalchemy.orm import Session
import hashlib
from datetime import datetime

from backend.database.models import User


def create_user_db(session: Session, name, password, rol):
    # Crear el objeto userabout:blank#blocked
    user = User(
        name=name,
        password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
        rol=rol.upper(),
    )
    # Agregar el user a la sesión y confirmar los cambios
    session.add(user)
    session.commit()
    return user


def update_user_db(session: Session, user_id: str, user: dict):
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.items():
            if hasattr(db_user, key) and getattr(db_user, key) != value:
                if key == 'password' and value is not None:
                    value = hashlib.sha256(value.encode('utf-8')).hexdigest()
                if value is not None:
                    setattr(db_user, key, value)
        db_user.modified_date = datetime.now()
        session.commit()
        return db_user
    return None

def delete_user_db(session: Session, user_id: str):
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user:
        session.delete(db_user)
        session.commit()
        return True
    return False
