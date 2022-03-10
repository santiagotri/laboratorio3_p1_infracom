#import socket
#import sys
from cliente import Cliente


numClientes = 10
direccionServidor = "localhost"
puertoInicial = 10000

clientes = []

for i in range(numClientes):
    clienteNuevo = Cliente(direccionServidor, puertoInicial)
    clientes.append(clienteNuevo)


print(len(clientes))
