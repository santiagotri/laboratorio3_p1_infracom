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
numClientes = 10
direccionServidor = "0.0.0.0"
puertoInicial = 10000

logging.basicConfig(filename=nombreArchivoLogging, level=logging.DEBUG)

clientes = []

barrera = threading.Barrier(numClientes+1)

def imprimir (mensaje):
    msjeAImprimir = ("MAIN: " + str(mensaje))
    if (IMPRIMIR_MENSAJES_MAIN): print(msjeAImprimir)
    logging.info(msjeAImprimir)

imprimir("creando "+ str(numClientes) + " clientes")
for i in range(numClientes):
    clienteNuevo = Cliente(direccionServidor, puertoInicial, i, IMPRIMIR_MENSAJES_CLIENTE,nombreArchivoLogging,barrera)
    clientes.append(clienteNuevo)


for i in clientes:
    i.start()

while barrera.n_waiting != numClientes:
    pass

imprimir("Se han creado correctamente todos los clientes, iniciando las conexiones en 5 segundos. Cada conexion será lanzada con 1 segundo de diferencia")
time.sleep(5)

barrera.wait()
barrera.reset()

for i in clientes:
    i.join()

imprimir("Ejecucion terminada")


