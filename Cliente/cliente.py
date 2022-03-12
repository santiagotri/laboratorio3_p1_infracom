import socket
import os
import time
import threading
import tqdm
import logging

class Cliente(threading.Thread):

    # Parametros
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    # Variables globales
    imprimirMensajes = False
    id = -1
    logging = logging
    puerto = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear el puerto TCP/IP socket

    #Esta funcion se encarga de imprimir la informacion en consola cuando es solicitado y realizar el logging
    def imprimir(self, mensaje):
        msjeAImprimir = ("CLIENTE "+ str(self.id) +": " + str(mensaje))
        if(self.imprimirMensajes): print(msjeAImprimir)
        self.logging.info(msjeAImprimir)

    #Constructor 🔧👷🏻‍♂️
    def __init__(self, pDireccionServidor, pNumPuerto, id, pImprimir_mensajes,nombreArchivoLogging,barrera):
        super(Cliente, self).__init__()
        self.logging.basicConfig(filename=nombreArchivoLogging, encoding='utf-8', level=logging.DEBUG)
        self.direccion_servidor = (pDireccionServidor,pNumPuerto)
        self.imprimirMensajes = pImprimir_mensajes
        self.id = id
        self.imprimir("creado. Entrando en espera")
        self.barrera = barrera


    #Metodo run del super(), ejecutada cuando el thread empieza con el start()
    def run(self):
        self.barrera.wait()
        #self.imprimir("durmiendo por " + str(self.id) + " segundos")
        time.sleep(self.id)
        self.imprimir("Iniciando proceso de conexion")
        self.realizar_conexion()

    #Realiza la conexion al servidor con los parametros establecidos en el contreuctor
    def realizar_conexion(self):
        self.imprimir("Intentando conectarse a " + str(self.direccion_servidor[0]) + " usando el puerto " + str(self.direccion_servidor[1]))
        try:
            self.puerto.connect(self.direccion_servidor)
            self.imprimir("Conexion exitosa! Esperando al envio")
            self.recibir_archivo()
        except Exception as e:
            self.imprimir("Ha fallado el intento de conexion (" + str(e) + ")")

    #Escuchar al servidor para recibir el archivo enviado.
    def recibir_archivo(self):
        self.puerto.listen()
        self.imprimir("Esperando al envio de un archivo")
        received = self.socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        self.imprimir("Recibiendo archivo "+ filename + " de tamaño " + str(filesize))
        ruta_a_guardar = "archivos_recibidos/cliente"+str(self.id)+"/"+filename
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(ruta_a_guardar, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.puerto.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        # close the puerto
        self.imprimir("Archivo transferido exitosamente y almacenado en " + ruta_a_guardar)
        self.puerto.close()