def onda(amp, frec, x, offset, tipo_senal):
    xp = 0.0512 * frec - 0.0512
    yp = 6.4 * amp + 64

    posicion = x % xp

    tipo_senal = tipo_senal.lower()

    if tipo_senal == "pwm":
        if posicion < xp / 2:
            return yp + offset
        else:
            return -yp + offset

    elif tipo_senal == "sierra":
        pendiente = (2 * yp) / xp
        y = -yp + pendiente * posicion
        return y + offset

    elif tipo_senal == "cosenoidal":
        angulo = (2 * 3.141592653589793 * posicion) / xp
        y = yp * (1 - (angulo**2) / 2 + (angulo**4) / 24 - (angulo**6) / 720)
        return y + offset

    else:
        print("Función no conocida:", tipo_senal)

amp = float(input("Introduce los voltios pico: "))
frec = float(input("Introduce la frecuencia en Hz: "))
x = float(input("Introduce la coordenada X: "))
offset = float(input("Introduce el offset: "))
tipo_senal = input("Introduce el tipo de señal (pwm, sierra, cosenoidal): ")

y = onda(amp, frec, x, offset, tipo_senal)
print(f"La coordenada Y para X={x} es {y}")
