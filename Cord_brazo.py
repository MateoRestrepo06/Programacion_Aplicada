import board
import pwmio
import wifi
import socketpool
from machine import ADC, I2C, Pin
import ssd1306
import math

servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

vrx = ADC(Pin(26))
vry = ADC(Pin(27))

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

def leer_joystick():
    x = vrx.read_u16()
    y = vry.read_u16()
    return x, y

def dibujar_brazo(value1, value2):
    oled.fill(0)
    base_x, base_y = 64, 32
    length1 = 30
    length2 = 20

    angle1 = map_range(value1, 0, 100, 0, 180)
    angle2 = map_range(value2, 0, 100, 0, 180)

    x1 = base_x + int(length1 * math.cos(math.radians(angle1)))
    y1 = base_y - int(length1 * math.sin(math.radians(angle1)))

    x2 = x1 + int(length2 * math.cos(math.radians(angle1 + angle2)))
    y2 = y1 - int(length2 * math.sin(math.radians(angle1 + angle2)))

    oled.line(base_x, base_y, x1, y1, 1)
    oled.line(x1, y1, x2, y2, 1)
    oled.show()

try:
    wifi.radio.connect("Ejemplo", "12345678")
    print(f"Conectado a la Wi-Fi, IP: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"Error al conectar a la Wi-Fi: {e}")
    raise

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
ip_address = str(wifi.radio.ipv4_address)

try:
    server.bind((ip_address, 80))
except OSError as e:
    print(f"Error al enlazar el socket: {e}")
    server.close()
    raise

server.listen(1)
server.settimeout(10)

print(f"Servidor iniciado en http://{ip_address}")

def handle_request(request):
    try:
        if '/update_servos' in request:
            params = request.split(" ")[1].split("?")[1].split("&")
            request_dict = {param.split("=")[0]: param.split("=")[1] for param in params}
            value1 = float(request_dict.get('value1', 0))
            value2 = float(request_dict.get('value2', 0))

            mapped_value_Principal = map_range(value1, 0, 100, 1500, 8000)
            mapped_value_Secundario = map_range(value2, 0, 100, 1500, 4000)

            servo_Principal.duty_cycle = mapped_value_Principal
            servo_Secundario.duty_cycle = mapped_value_Secundario

            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
        else:
            try:
                with open("movimiento.html", 'r') as file:
                    response = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response}"
            except OSError:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found"
    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError: {str(e)}"
    return response

while True:
    try:
        client_socket, client_address = server.accept()
        print(f"Conexión desde {client_address}")

        buffer = bytearray(1024)
        num_bytes = client_socket.recv_into(buffer)
        request = buffer[:num_bytes].decode("utf-8").strip()

        response = handle_request(request)

        x, y = leer_joystick()

        value1 = map_range(x, 0, 65535, 0, 100)
        value2 = map_range(y, 0, 65535, 0, 100)

        mapped_value_Principal = map_range(value1, 0, 100, 1500, 8000)
        mapped_value_Secundario = map_range(value2, 0, 100, 1500, 4000)

        servo_Principal.duty_cycle = mapped_value_Principal
        servo_Secundario.duty_cycle = mapped_value_Secundario

        dibujar_brazo(value1, value2)

        client_socket.send(response.encode("utf-8"))
        client_socket.close()
    except OSError as e:
        print(f"Error en el servidor: {e}")
continue