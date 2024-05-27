from sqlalchemy.orm import Session
from datetime import datetime
import random
import string

from backend.database.models import Usuario

def crear_usuario(session: Session, password, nombre, rol):
    # Crear el objeto usuario
    usuario = Usuario(
        password=password,
        nombre=nombre,
        rol=rol,
    )

    # Agregar el usuario a la sesión y confirmar los cambios
    session.add(usuario)
    session.commit()

    return usuario

