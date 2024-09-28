import machine
import math
from adafruit_ssd1306 import SSD1306_I2C
import busio
import board

i2c = busio.I2C(board.GP5, board.GP4)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

l1 = 20
l2 = 15
l3 = 10
pasos = 100

adc_x = machine.ADC(26)
adc_y = machine.ADC(27)

def leer_x():
    valor_inicial= adc_x.read_u16()
    valor_x = (valor_inicial / 65535) * 2 - 1
    return valor_x

def leer_y():
    valor_inicial = adc_y.read_u16()
    valor_y = (valor_inicial / 65535) * 2 - 1
    return valor_y

def curva_bezier(t, P0, P1, P2, P3):
    return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

def draw_arm(oled, theta1, theta2, theta3):
    oled.fill(0)

    x0, y0 = 64, 32

    x1 = int(x0 + l1 * math.cos(theta1))
    y1 = int(y0 + l1 * math.sin(theta1))
    x2 = int(x1 + l2 * math.cos(theta1 + theta2))
    y2 = int(y1 + l2 * math.sin(theta1 + theta2))
    x3 = int(x2 + l3 * math.cos(theta1 + theta2 + theta3))
    y3 = int(y2 + l3 * math.sin(theta1 + theta2 + theta3))

    oled.line(x0, y0, x1, y1, 1)
    oled.line(x1, y1, x2, y2, 1)
    oled.line(x2, y2, x3, y3, 1)
    oled.show()

P0x, P0y = 64, 32
P3x, P3y = 100, 50
d = 15

P1x, P1y = P0x, P0y + d
P2x, P2y = P3x, P3y + d

for i in range(pasos):
    t = i / (pasos - 1)

    Px = curva_bezier(t, P0x, P1x, P2x, P3x)
    Py = curva_bezier(t, P0y, P1y, P2y, P3y)

    d_actual = math.sqrt(Px**2 + Py**2)

    if Px != 0:
        theta1 = math.atan2(Py, Px)
    else:
        theta1 = math.pi / 2 if Py > 0 else -math.pi / 2

    theta2 = math.acos((l1**2 + d_actual**2 - l2**2) / (2 * l1 * d_actual))
    theta3 = math.acos((l2**2 + l3**2 - d_actual**2) / (2 * l2 * l3))

    draw_arm(oled, theta1, theta2, theta3)
