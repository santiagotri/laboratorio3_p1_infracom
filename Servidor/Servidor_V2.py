
import socket
from threading import Thread

import sys
import socket
import tqdm
import os
import logging
import datetime
import time

BUFFER_SIZE = 1024
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
 
    def __init__(self, s, address): 
        Thread.__init__(self)
        self.ip = address[0]
        self.port = address[1]
        self.address = address
        self.s = s
        print(f"[+] Nuevo cliente en: {self.ip}:{str(self.port)}")
        logging.info(f"[+] Nuevo cliente en: {self.ip}:{str(self.port)}")

 
    def run(self): 

        # --> ARCHIVO PRINCIPAL

       try:

          # --> Hash

          Hfile = hash_file(filename)

          self.s.sendto(f"{Hfile}".encode(), self.address)
          logging.info("Se envio correctamente el hash del archivo !")

          time.sleep(1.5)

          # --> File

          self.s.sendto(f"{filename}{SEPARATOR}{filesize}".encode(), self.address)
          logging.info(f"Enviando el archivo {filename} de tamano {filesize}".encode())

          progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

          self.tiempo_total = time.time()
          with open(filename, "rb") as f:

              while True:

                  bytes_read = f.read(BUFFER_SIZE)

                  self.s.sendto(bytes_read, self.address)
                  progress.update(len(bytes_read))

                  if not bytes_read:
                      break

          progress.close()
          self.tiempo_total= time.time() - self.tiempo_total
          logging.info("Se envio correctamente el archivo principal !")

          logging.info(
              f"Total_de_bytes_recibidos:{str(filesize)} - Tiempo_tranferencia:" +
              str(round(self.tiempo_total, 3)) +
              "segundos - Tasa_transferencia_promedio:" +
              str(round(filesize / self.tiempo_total, 3)) + "B/s")            

       finally:
          pass

# --------------------------------------------------------------------------

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <host> <port> <listen> <file>")
    sys.exit(1)
 
HOST, PORT, NUMBER = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

filename = f"{sys.argv[4]}MB.bin"
filesize = os.path.getsize(filename)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # --> """ UDP """
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind((HOST, PORT))
threads = [] 
 
try:

    while True: 

        #s.listen(NUMBER) 
        logging.info(f"Server listening in {HOST} {PORT}")
        print(f"Server listening in {HOST} {PORT}")

        
        address = s.recvfrom(1024)[1]
        newthread = ClientThread(s, address)  
        threads.append(newthread) 

        if len(threads) == NUMBER:

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            break

except KeyboardInterrupt:
    print('Interrupted!')