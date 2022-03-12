#import socket
#import sys
from cliente import Cliente
import threading

IMPRIMIR_MENSAJES_CLIENTE = True
IMPRIMIR_MENSAJES_MAIN = True

numClientes = 10
direccionServidor = "localhost"
puertoInicial = 10000

clientes = []


def imprimir (mensaje):
    print("MAIN: " + str(mensaje))


imprimir("creando "+ str(numClientes) + " clientes")
for i in range(numClientes):
    clienteNuevo = Cliente(direccionServidor, puertoInicial, i, IMPRIMIR_MENSAJES_CLIENTE)
    clientes.append(clienteNuevo)

for i in clientes:
    i.start()


print(len(clientes))

