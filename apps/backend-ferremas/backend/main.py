import requests
import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker


from backend.create_cat_prod import create_category_and_product
from backend.database.models import Product, Base, Category, User
from backend.create_user import create_user
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
            session.query(Product).first()
            logger.info("La base de datos ya esta inicializada.")
        except Exception as e:
            Base.metadata.create_all(engine)
            logger.info("Inicializando la base de datos...")
            create_category_and_product(session)
           
            
@app.post("/create-user", tags=["USER"])
async def create_users(password, name, rol):
    with Session() as session:
        try:
            create_user(session, password, name, rol)
            return {"message": "Usuario creado correctamente"}
        except Exception as e:
            if "UNIQUE constraint failed: user.name" in str(e):
                return {"message": "Usuario ya creado"}


@app.get("/login")
async def login(username: str, password: str):
    with Session() as session:
        user = session.query(User).filter(User.name == username).first()
        if user:
            if verify_password(password, user.password):
                return {"message": "Inicio de sesión exitoso"}
            else:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/get-user", tags=["TABLES"])
async def obtener_usuario():
    with Session() as session:
        user = session.query(User).all()
        return user


@app.get("/get-product", tags=["TABLES"])
async def obtener_productos():
    with Session() as session:
        product = session.query(Product).all()
        return product


@app.get("/get-category", tags=["TABLES"])
async def obtener_productos():
    with Session() as session:
        category = session.query(Category).all()
        return category


@app.get("/get-dolar", tags=["Dolar"])
async def obtener_dolar():
    url = 'https://mindicador.cl/api/dolar'
    response = requests.get(url)
    dolar = response.json()["serie"][0]["valor"]
    return dolar


if __name__ == "__main__":
    print("Hello World")
