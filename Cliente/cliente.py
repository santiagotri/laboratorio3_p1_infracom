import socket
import sys
import time
import threading

class Cliente(threading.Thread):
    direccion_servidor = ()
    imprimirMensajes = False
    id = -1


    # Crear el puerto TCP/IP socket
    puerto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def imprimir(self, mensaje):
        print("CLIENTE "+ str(self.id) +": " + str(mensaje))

    def __init__(self, pDireccionServidor, pNumPuerto, id, pImprimir_mensajes):
        super(Cliente, self).__init__()
        self.direccion_servidor = (pDireccionServidor,pNumPuerto+id)
        self.imprimirMensajes = pImprimir_mensajes
        self.id = id
        self.imprimir("creado. Puerto " + str(self.direccion_servidor[1]))

    def run(self):
        self.imprimir("durmiendo por " + str(self.id) + " segundos")
        time.sleep(self.id)
        self.imprimir("Listo")

    #puerto.connect(direccion_servidor)

