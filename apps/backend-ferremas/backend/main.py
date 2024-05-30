import requests
import logging
import asyncio
import paypalrestsdk
import base64
from fastapi import FastAPI, File, HTTPException, Depends, UploadFile, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

from backend.crud_productos import convert_image_to_binary, create_product_db, update_product_db, delete_product_db
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

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AdnK_iYp1pW_fD8vavvCQUdYeBhXxIQddQZh6ooenQADph8dlzFeGtrjvgEm99q_QJyWC9l8nU9PM_U4",
    "client_secret": "EP44dwSslrRYbMv7vmTNh747aqMuzK4EdS34gqlMjCOlcgfLXCuJDK3HFMtltzgd7_aCTOb0EFM7qQbg"
})

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
                return {'user': user.name, 'password': user.password, 'rol': user.rol}
            else:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/get-users", tags=["CRUD User"])
async def get_users():
    with Session() as session:
        user = session.query(User).all()
        return user


@app.delete("/delete-user", tags=["CRUD User"])
async def delete_user(user_id):
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
        products = session.query(Product).all()
        result = []
        for product in products:
            # Convertir la imagen a base64 si existe
            if product.image:
                image_base64 = base64.b64encode(product.image).decode('utf-8')
            else:
                image_base64 = None

            # Agregar el producto con la imagen codificada a la lista de resultados
            result.append({
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "category": product.category,
                "brand": product.brand,
                "image": image_base64,  # Imagen codificada en base64
                "price": product.price,
                "enable": product.enable if hasattr(product, 'enable') else None  # Asegúrate de que 'enable' existe
            })

        return result


@app.get("/get-product", tags=["CRUD Productos"])
async def get_product(product_id):
    with Session() as session:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Convertir la imagen a base64 si existe
        if product.image:
            product.image = base64.b64encode(product.image).decode('utf-8')
        else:
            product.image = None

        # Devolver todos los datos excepto la imagen binaria directamente
        return product

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
async def update_product(product_id: str, name=None, stock=None ,category=None, brand=None, image: UploadFile=None, price=None, enable=None):
    if image:
        image = await convert_image_to_binary(image)

    product = {'name': name, 'stock': stock , 'category': category, 'brand': brand, 'image': image, 'price': price, 'enable': enable}

    # Crear una sesión y ejecutar la función síncrona en un hilo separado
    def db_operation(session, product_id, product):
        return update_product_db(session, product_id, product)

    with Session() as session:
        loop = asyncio.get_running_loop()
        updated_product_db = await loop.run_in_executor(None, db_operation, session, product_id, product)

        if updated_product_db is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"detail": "Producto actualizado exitosamente"}


@app.post("/create-payment")
async def create_payment(total: float):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(total),  # Ahora el total es dinámico
                "currency": "USD"
            },
            "description": "Descripción de la transacción de pago."
        }],
        "redirect_urls": {
            "return_url": "http://localhost:4200/carrito",
            "cancel_url": "http://localhost:4200/carrito"
        }
    })

    if payment.create():
        print("Pago creado exitosamente")
        for link in payment.links:
            if link.rel == "approval_url":
                # Captura la URL para redirigir al usuario
                approval_url = str(link.href)
                return {"approval_url": approval_url}
    else:
        return {"error": "Ocurrió un error al crear el pago"}


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
