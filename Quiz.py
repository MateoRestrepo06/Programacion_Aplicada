import board
import digitalio 
import wifi
import socketpool

wifi.import("SSID","Pasword")

n=r.find('led=1')
if n>-1:
  Led1=Prendido
  return Led1
n=r.find('led=2')
if n>-1:
  Led2=Prendido
  return Led2
else n = -1:
  print ("No hay información sobre el LED")
Estado=("Led1", "Led2")
wifi.serv("URL.html",'r')
  response =(Estado)