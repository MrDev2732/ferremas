import requests
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

from backend.create_products import crear_categorias_y_productos
from backend.database.models import Producto, Base


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


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)
    with Session() as session:
        crear_categorias_y_productos(session)


@app.get("/obtener-productos", tags=["Productos"])
async def obtener_productos():
    with Session() as session:
        productos = session.query(Producto).all()
        return productos


@app.get("/obtener-dolar", tags=["Dolar"])
async def obtener_dolar():
    url = 'https://mindicador.cl/api/dolar'
    response = requests.get(url)
    dolar = response.json()["serie"][0]["valor"]
    return dolar


if __name__ == "__main__":
    print("Hola mundo")
