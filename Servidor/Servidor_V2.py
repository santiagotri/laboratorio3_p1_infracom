
import socket
from threading import Thread

import sys
import socket
import tqdm
import os
import logging
import datetime
import time

BUFFER_SIZE = 10485760
SEPARATOR = "<SEPARATOR>"

# -------------------------------------------------------------------------------------------------

import hashlib

def hash_file(filename):

   h = hashlib.sha1()

   with open(filename,'rb') as file:

       chunk = 0
       while chunk != b'':

           chunk = file.read(1024)
           h.update(chunk)

   return h.hexdigest()
# -------------------------------------------------------------------------------------------------

fecha = str(datetime.datetime.now()).split(" ")
hora = fecha[1].split(":")
nombreArchivoLogging = f"Logs/{fecha[0]}-{hora[0]}-{hora[1]}-{hora[2]}-log.log"
logging.basicConfig(filename=nombreArchivoLogging, level=logging.DEBUG)

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port, c): 
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = c
        print(f"[+] Nuevo cliente en: {ip}:{str(port)}")
        logging.info(f"[+] Nuevo cliente en: {ip}:{str(port)}")

 
    def run(self): 

        # --> ARCHIVO PRINCIPAL

        try:

            # --> Hash

            Hfile = hash_file(filename)

            self.conn.send(f"{Hfile}".encode())
            logging.info("Se envio correctamente el hash del archivo !")

            time.sleep(1.5)

            # --> File

            self.conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
            logging.info(f"Enviando el archivo {filename} de tamano {filesize}".encode())

            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            self.tiempo_total = time.time()
            with open(filename, "rb") as f:

                while True:

                    bytes_read = f.read(BUFFER_SIZE)

                    self.conn.send(bytes_read)
                    progress.update(len(bytes_read))

                    if not bytes_read:
                        break

            progress.close()
            self.tiempo_total= time.time() - self.tiempo_total
            logging.info("Se envio correctamente el archivo principal !")            

        finally:

            logging.INFO("Total_de_bytes_recibidos:" + str(filesize) + " - Tiempo_tranferencia:" + str(round(self.tiempo_total,3))+"segundos - Tasa_transferencia_promedio:" + str(round(filesize/self.tiempo_total,3))+"B/s")
            self.conn.close()

# --------------------------------------------------------------------------

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <host> <port> <listen> <file>")
    sys.exit(1)
 
HOST, PORT, NUMBER = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

filename = f"{sys.argv[4]}MB.bin"
filesize = os.path.getsize(filename)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind((HOST, PORT))
threads = [] 
 
try:

    while True: 

        s.listen(NUMBER) 
        logging.info(f"Server listening in {HOST} {PORT}")
        print(f"Server listening in {HOST} {PORT}")

        (conn, (ip,port)) = s.accept() 
        newthread = ClientThread(ip,port, conn)  
        threads.append(newthread) 

        if len(threads) == NUMBER:

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            break

except KeyboardInterrupt:
    print('Interrupted!')