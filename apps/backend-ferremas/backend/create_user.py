from sqlalchemy.orm import Session
import hashlib

from backend.database.models import User


def create_user(session: Session, password, name, rol):
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
