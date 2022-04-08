import socket
import os
import time
import threading
import tqdm
import logging
import traceback
import hashlib


class Cliente(threading.Thread):

    # Parametros
    BUFFER_SIZE = 1024
    SEPARATOR = "<SEPARATOR>"

    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)

    HOST = "localhost"
    PORT = 20001

    # Variables globales
    imprimirMensajes = False
    id = -1
    logging = logging

    #Esta funcion se encarga de imprimir la informacion en consola cuando es solicitado y realizar el logging
    def imprimir(self, mensaje):
        msjeAImprimir = ("CLIENTE "+ str(self.id) +": " + str(mensaje))
        if(self.imprimirMensajes): tqdm.tqdm.write(msjeAImprimir)
        self.logging.info(msjeAImprimir)

    def imprimir_error(self, mensaje):
        msjeAImprimir = ("CLIENTE " + str(self.id) + ": " + str(mensaje))
        if (self.imprimirMensajes): tqdm.tqdm.write(msjeAImprimir)
        self.logging.error(msjeAImprimir)

    #Constructor 🔧👷🏻‍♂️
    def __init__(self, id, pImprimir_mensajes,nombreArchivoLogging,barrera,pdireccion,puertoinicial,segundosEntreThreat, pBUFFER_SIZE):
        super(Cliente, self).__init__()
        self.logging.basicConfig(filename=nombreArchivoLogging, encoding='utf-8', level=logging.DEBUG)
        self.imprimirMensajes = pImprimir_mensajes
        self.id = id
        self.imprimir("creado. Entrando en espera")
        self.barrera = barrera
        self.puerto = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.PORT = puertoinicial
        self.HOST = pdireccion
        self.segundosEntreThreat=(segundosEntreThreat*id)
        self.BUFFER_SIZE = pBUFFER_SIZE
        self.msgFromClient = str(pBUFFER_SIZE)
        self.bytesToSend = str.encode(self.msgFromClient)

    #Metodo run del super(), ejecutada cuando el thread empieza con el start()
    def run(self):
        self.barrera.wait()
        #self.imprimir("durmiendo por " + str(self.id) + " segundos")
        time.sleep(self.segundosEntreThreat)
        self.imprimir("Iniciando proceso de conexion")
        self.realizar_conexion()

    #Realiza la conexion al servidor con los parametros establecidos en el contreuctor
    def realizar_conexion(self):
        self.imprimir("Intentando enviar mensaje a " + str(self.HOST) + " usando el puerto " + str(self.PORT))
        try:
            self.puerto.sendto(self.bytesToSend, (self.HOST, self.PORT))
            self.imprimir("Mensaje enviado exitosamente! Esperando al envio por parte del servidor")
            self.recibir_archivo()
        except Exception as e:
            self.imprimir_error("Ha fallado el intento de envío (" + str(e) + ")")
            traceback.print_exc()

    #Escuchar al servidor para recibir el archivo enviado.
    def recibir_archivo(self):
        try:
            self.imprimir("Esperando al envio de un archivo")
            hash_recibido = self.puerto.recvfrom(self.BUFFER_SIZE)
            received = self.puerto.recvfrom(self.BUFFER_SIZE)
            #print(hash_recibido[0].decode())
            #print(received[0].decode())
            hash_recibido = hash_recibido[0].decode()
            received = received[0].decode()
            filename, filesize = received.split(self.SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            self.imprimir("Recibiendo archivo " + filename + " de tamaño " + str(filesize))
            ruta_a_guardar = "archivos_recibidos/cliente" + str(self.id) + "_" + filename
            progress = tqdm.tqdm(range(filesize), f"Cliente{str(self.id)}: Recibiendo {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            self.tiempo_total = time.time()
            self.cantidad_recibida = 0
            with open(ruta_a_guardar, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = self.puerto.recvfrom(self.BUFFER_SIZE)
                    bytes_read = bytes_read[0]
                    #print('recibiendo:' + str(len(str(bytes_read))))
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
                    self.cantidad_recibida += len(bytes_read)

                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        print("hola")
                        break
            progress.close()
            self.tiempo_total= time.time() - self.tiempo_total
            self.barrera.wait()
            """
            hash_calculado = self.hash_file(ruta_a_guardar)
            if(hash_calculado==hash_recibido):
                self.imprimir("Integridad verificada correctamente (Hash OK)")
            else:
                self.imprimir_error("¡Error de integridad!")
                self.imprimir_error(str(hash_calculado))
                self.imprimir_error(str(hash_recibido))
            """
            self.imprimir("Total_de_bytes_recibidos:" + str(self.cantidad_recibida) + " - Tiempo_tranferencia:" + str(round(self.tiempo_total,3))+"segundos - Tasa_transferencia_promedio:" + str(round(filesize/self.tiempo_total,3))+"B/s")
        finally:
            self.puerto.close()




    # -------------------------------------------------------------------------------------------------

    def hash_file(self, filename):

        h = hashlib.sha1()

        with open(filename, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)

        return h.hexdigest()
    # -------------------------------------------------------------------------------------------------
