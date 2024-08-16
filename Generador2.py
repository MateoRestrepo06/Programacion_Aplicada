def onda(amp, frec, x, offset):
    xp = 0.0512 * frec - 0.0512
    yp = 6.4 * amp + 64

    posicion = x % xp

    if posicion < xp / 2:
        return yp + offset
    else:
        return -yp + offset

amp = float(input("Introduce la amplitud: "))
frec = float(input("Introduce la frecuencia: "))
x = float(input("Introduce la coordenada X: "))
offset = float(input("Introduce el desplazamiento: "))

y = onda(amp, frec, x, offset)
print(f"La coordenada Y para X={x} es {y}")

