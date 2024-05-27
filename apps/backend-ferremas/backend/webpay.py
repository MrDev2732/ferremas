from transbank.webpay.webpay_plus.transaction import Transaction
import webbrowser
CODIGO_COMERCIO = '597055555532'
API_KEY = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
import time
# Crear una instancia de Transaction
tx = Transaction()

# Configurar la instancia para integración
tx.configure_for_integration(CODIGO_COMERCIO, API_KEY)

def webpay_transaccion(buy_order, session_id, amount, return_url):
    response = tx.create(buy_order, session_id, amount, return_url)

    token = response['token']
    url = f"{response['url']}/{token}"
    webbrowser.open(url, new=2)
    time.sleep(10)
    resp = tx.commit(token)
    # Confirmar la transacción

webpay_transaccion("1", "1", 100, "https://github.com/MrDev2732/ferremas")
