import hashlib

def verify_password(plain_password, hashed_password):
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada.

    Args:
        plain_password (str): La contraseña en texto plano a verificar.
        hashed_password (str): La contraseña hasheada almacenada en la base de datos.

    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    
    hashed_plain_password = hashlib.sha256((plain_password).encode()).hexdigest()

    return hashed_plain_password == hashed_password