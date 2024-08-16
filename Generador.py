def onda(amp, frec, x):
    xp = 0.0512 * frec - 0.0512
    yp = 6.4 * amp + 64

    posicion = x % xp

    if posicion < xp / 2:
        return yp
    else:
        return -yp
        

