from sqlalchemy.orm import Session
from datetime import datetime
import random
import string

from backend.database.models import Usuario

def crear_usuario(session: Session, user_id, password, nombre, rol):
    # Crear el objeto usuario
    usuario = Usuario(
        id=user_id,
        password=password,
        nombre=nombre,
        rol=rol,
    )

    # Agregar el usuario a la sesión y confirmar los cambios
    session.add(usuario)
    session.commit()

    return usuario

