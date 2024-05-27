import requests
import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker


from backend.create_cat_prod import crear_categorias_y_productos
from backend.database.models import Producto, Base, Categoria, Usuario
from backend.create_user import crear_usuario
from backend.verify_password import verify_password

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:     %(name)s - %(message)s')
logger = logging.getLogger(__name__)


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
    with Session() as session:
        try:
            session.query(Producto).first()
            logger.info("La base de datos ya esta inicializada.")
        except Exception as e:
            Base.metadata.create_all(engine)
            logger.info("Inicializando la base de datos...")
            crear_categorias_y_productos(session)
           
            
@app.post("/crear-usuario", tags=["USUARIOS"])
async def create_user(password, nombre, rol):
    with Session() as session:
        try:
            crear_usuario(session, password, nombre, rol)
            return {"message": "Usuario creado correctamente"}
        except Exception as e:
            if "UNIQUE constraint failed: usuario.nombre" in str(e):
                return {"message": "Usuario ya creado"}


@app.get("/login")
async def login(username: str, password: str):
    with Session() as session:
        user = session.query(Usuario).filter(Usuario.nombre == username).first()
        if user:
            logger.info(user.password)
            logger.info(password)
            if verify_password(password, user.password):
                return {"message": "Inicio de sesión exitoso"}
            else:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/obtener-usuario", tags=["TABLAS"])
async def obtener_usuario():
    with Session() as session:
        usuario = session.query(Usuario).all()
        return usuario


@app.get("/obtener-productos", tags=["TABLAS"])
async def obtener_productos():
    with Session() as session:
        productos = session.query(Producto).all()
        return productos


@app.get("/obtener-categorias", tags=["TABLAS"])
async def obtener_productos():
    with Session() as session:
        categorias = session.query(Categoria).all()
        return categorias


@app.get("/obtener-dolar", tags=["Dolar"])
async def obtener_dolar():
    url = 'https://mindicador.cl/api/dolar'
    response = requests.get(url)
    dolar = response.json()["serie"][0]["valor"]
    return dolar


if __name__ == "__main__":
    print("Hello World")
