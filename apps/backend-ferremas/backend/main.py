import requests
import logging
import asyncio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

from backend.crud_productos import create_product_db, update_product_db, delete_product_db
from backend.crud_users import create_user_db, update_user_db, delete_user_db
from backend.create_db import create_category_and_product
from backend.database.models import Product, Base, Category, User
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
           
            
@app.post("/create-user", tags=["CRUD User"])
async def create_users(name, password, rol):
    with Session() as session:
        try:
            create_user_db(session, name, password, rol)
            return {"message": "Usuario creado correctamente"}
        except Exception as e:
            if "UNIQUE constraint failed: user.name" in str(e):
                return {"message": "Usuario ya creado"}


@app.get("/login", tags=["CRUD User"])
async def login(username: str, password: str):
    with Session() as session:
        user = session.query(User).filter(User.name == username).first()
        if user:
            if verify_password(password, user.password):
                return True
            else:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/get-user", tags=["CRUD User"])
async def obtener_usuario():
    with Session() as session:
        user = session.query(User).all()
        return user


@app.delete("/delete-user", tags=["CRUD User"])
async def delete_product(user_id):
    with Session() as session:
        delete_user_db(session, user_id)
        return {"detail": "Usuario eliminado exitosamente"}


@app.put("/update-user", tags=["CRUD User"])
async def update_user(user_id: int, name: str, password: str, rol: str):
    user_data = {'name': name, 'password': password, 'rol': rol}

    # Crear una sesión y ejecutar la función síncrona en un hilo separado
    def db_operation(session, user_id, user_data):
        return update_user_db(session, user_id, user_data)

    with Session() as session:
        loop = asyncio.get_running_loop()
        updated_user_db = await loop.run_in_executor(None, db_operation, session, user_id, user_data)

        if updated_user_db is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"detail": "Usuario actualizado exitosamente"}


@app.get("/get-products", tags=["CRUD Productos"])
async def get_products():
    with Session() as session:
        product = session.query(Product).all()
        return product


@app.get("/get-product", tags=["CRUD Productos"])
async def get_product(product_id):
    with Session() as session:
        return session.query(Product).filter(Product.id == product_id).first()


@app.post("/create-product/", tags=["CRUD Productos"])
async def create_product(category, product, brand):
    with Session() as session:
        create_product_db(session, category, product, brand)
        return {"detail": "Producto creado exitosamente"}


@app.delete("/delete-product", tags=["CRUD Productos"])
async def delete_product(product_id):
    with Session() as session:
        delete_product_db(session, product_id)
        return {"detail": "Producto eliminado exitosamente"}


@app.put("/update-product", tags=["CRUD Productos"])
async def update_product(product_id: str, name=None, category=None, brand=None, image=None, price=None, enable=None):
    product = {'name': name, 'category': category, 'brand': brand, 'image': image, 'price': price, 'enable': enable}
    
    # Crear una sesión y ejecutar la función síncrona en un hilo separado
    def db_operation(session, product_id, product):
        return update_product_db(session, product_id, product)

    with Session() as session:
        loop = asyncio.get_running_loop()
        updated_product_db = await loop.run_in_executor(None, db_operation, session, product_id, product)
        
        if updated_product_db is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"detail": "Producto actualizado exitosamente"}


@app.get("/get-category", tags=["Categorias"])
async def obtener_categorias():
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
