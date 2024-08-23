import board
import digitalio
import wifi
import socketpool

# Conexión Wi-Fi
wifi.radio.connect("SSID", "Password")

# Definir los pines para los LEDs
led1 = digitalio.DigitalInOut(board.GP1)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP2)
led2.direction = digitalio.Direction.OUTPUT

# Crear un socket para manejar las solicitudes HTTP
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind(("0.0.0.0", 80))
server.listen(1)

def handle_request(request):
    r = str(request)

    # Verificar si la solicitud es para encender o apagar el LED 1
    n1 = r.find('led=1')
    if n1 > -1:
        led1.value = not led1.value  # Cambia el estado del LED 1
        estado_led1 = "prendido" if led1.value else "apagado"
    else:
        estado_led1 = "-1"

    # Verificar si la solicitud es para encender o apagar el LED 2
    n2 = r.find('led=2')
    if n2 > -1:
        led2.value = not led2.value  # Cambia el estado del LED 2
        estado_led2 = "prendido" if led2.value else "apagado"
    else:
        estado_led2 = "-1"

    # Crear la respuesta HTML
    response = f"""
    <html>
    <head>
        <title>Control de LEDs</title>
    </head>
    <body>
        <h1>Estado de los LEDs</h1>
        <p>LED 1: {estado_led1}</p>
        <p>LED 2: {estado_led2}</p>
        <a href="?led=1"><button>Toggle LED 1</button></a>
        <a href="?led=2"><button>Toggle LED 2</button></a>
    </body>
    </html>
    """
    return response

while True:
    conn, addr = server.accept()
    request = conn.recv(1024)
    response = handle_request(request)
    conn.send("HTTP/1.1 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("Connection: close\r\n\r\n")
    conn.sendall(response)
    conn.close()
