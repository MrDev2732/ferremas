from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, SQLModel, select, Session
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

from backend.database.models import Categoria, Producto, Base

engine = create_engine("sqlite:///database.sqlite3")
Session = sessionmaker(bind=engine)

app = FastAPI(
    title="API Ferremas",
    docs_url="/api/docs",
)
# Configurar CORS
origins = [
    "http://localhost:4200"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_scheme = APIKeyHeader(name="x-api-key")

access_tokens = {
    "11fc663c-0400-4bf4-a123-62e98d22f24c",
    "73695659-cc2b-4b32-ad0e-1f91bbefff08",
    # Diccionario de tokens
}


# Función para validar el token de acceso
async def validate_token(api_key: str = Depends(api_key_scheme)):
    if api_key not in access_tokens:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de acceso inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key


def crear_categorias_y_productos(session: Session):
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
                crear_productos(session, subcategoria, productos, marcas)
        else:
            crear_productos(session, categoria_principal, subcategorias, marcas)


def crear_productos(session: Session, categoria, productos, marcas):
    for producto in productos:
        codigo_producto = f'{producto[:3].upper()}-{random.randint(100, 999)}'
        now = datetime.now()
        precios = [
            {
                "fecha": now.isoformat(),
                "valor": random.randint(1, 100)
            }
        ]
        prod_obj = Producto(
            id=codigo_producto,
            marca=random.choice(marcas),
            name=producto,
            categoria=categoria,
            stock=random.randint(0, 100),
            imagen=None,
            enabled=True,
            created_date=now,
            modified_date=now,
            deleted_date=None,
            precios=precios
        )
        session.add(prod_obj)
    session.commit()


def get_or_create(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        # Asegurarse de que todos los campos NOT NULL tengan un valor predeterminado
        now = datetime.now()
        defaults = {
            'enabled': True,
            'created_date': now,
            'modified_date': now,
            'deleted_date': None  # Asumiendo que puede ser NULL
        }
        # Actualizar los valores predeterminados con cualquier valor proporcionado en kwargs
        defaults.update(kwargs)
        instance = model(**defaults)
        session.add(instance)
        session.commit()
        return instance


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)
    with Session() as session:
        crear_categorias_y_productos(session)


@app.get("/productos", tags=["Productos"])
async def obtener_productos():
    with Session() as session:
        productos = session.query(Producto).all()
        return productos


if __name__ == "__main__":
    print("Hola mundo")
