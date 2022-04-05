#import socket
#import sys
from cliente import Cliente
import logging
import datetime
import threading
import time

IMPRIMIR_MENSAJES_CLIENTE = True
IMPRIMIR_MENSAJES_MAIN = True
fecha = str(datetime.datetime.now()).split(" ")
hora = fecha[1].split(":")
nombreArchivoLogging = "Logs/"+fecha[0]+"-"+hora[0]+"-"+hora[1]+"-"+hora[2]+"-log.log"
numClientes = input("¿Cuantos clientes desea crear? {default: 3}")
if numClientes == "":
    numClientes = 3
else:
    numClientes = int(numClientes)

direccionServidor = input("Introduzca la direccion del servidor {default:localhost}")
if numClientes == "": direccionServidor = "localhost"
puertoInicial = input("¿Cual es el puerto en el que está escuchando el servidor? {default: 12345}")
if puertoInicial == "":
    puertoInicial = 12345
else:
    puertoInicial = int(puertoInicial)

segundosEntreThreat = input("¿Cada cuantos segundos desea enviar cada uno de los clientes? {default:1}")
if segundosEntreThreat == "":
    segundosEntreThreat = 1
else:
    segundosEntreThreat = int(segundosEntreThreat)

logging.basicConfig(filename=nombreArchivoLogging, level=logging.DEBUG)

clientes = []

barrera = threading.Barrier(numClientes+1)

def imprimir (mensaje):
    msjeAImprimir = ("MAIN: " + str(mensaje))
    if (IMPRIMIR_MENSAJES_MAIN): print(msjeAImprimir)
    logging.info(msjeAImprimir)

imprimir("creando "+ str(numClientes) + " clientes")
for i in range(numClientes):
    clienteNuevo = Cliente(i, IMPRIMIR_MENSAJES_CLIENTE,nombreArchivoLogging,barrera,direccionServidor,puertoInicial,segundosEntreThreat)
    clientes.append(clienteNuevo)


for i in clientes:
    i.start()

while barrera.n_waiting != numClientes:
    pass

imprimir("Se han creado correctamente todos los clientes, iniciando las conexiones en 5 segundos. Cada conexion será lanzada con "+str(segundosEntreThreat)+" segundo(s) de diferencia")
time.sleep(5)

barrera.wait()
barrera.reset()

while barrera.n_waiting != numClientes:
    pass

imprimir("Se han recibido todos los archivos. Se verificará Integridad para cada cliente.")
barrera.wait()
barrera.reset()

for i in clientes:
    i.join()
imprimir("Los archivos transferidos exitosamente fueron almacenados en \"archivos_recibidos/clienteX_Y\", donde X es el numero del cliente y Y el nombre original del archivo transferido")
imprimir("Ejecucion terminada")


