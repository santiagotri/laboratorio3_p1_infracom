import socket
import sys

class Cliente:
    direccion_servidor = ()
    # Crear el puerto TCP/IP socket
    puerto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    numerodos = 32

    def __init__(self, pDireccionServidor, pNumPuerto):
        self.direccion_servidor = (pDireccionServidor,pNumPuerto)
        self.numerodos = 2
        print (str(pNumPuerto))

    print(str(numerodos))
    print (str(len(direccion_servidor)))
    #puerto.connect(direccion_servidor)

