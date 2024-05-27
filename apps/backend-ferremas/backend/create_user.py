from sqlalchemy.orm import Session
from datetime import datetime
import random
import string
import hashlib


from backend.database.models import Usuario

def crear_usuario(session: Session, password, nombre, rol):
    # Crear el objeto usuario
    usuario = Usuario(
        password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
        nombre=nombre,
        rol=rol,
    )

    # Agregar el usuario a la sesión y confirmar los cambios
    session.add(usuario)
    session.commit()

    return usuario
