
import socket
from threading import Thread

import sys
import socket
import tqdm
import os
import logging
import datetime

BUFFER_SIZE = 4096

filename = "100MB.bin"
hash_filename = "hash.txt"
filesize = os.path.getsize(filename)
SEPARATOR = "<SEPARATOR>"

# -------------------------------------------------------------------------------------------------

# Python program to find the SHA-1 message digest of a file

# importing the hashlib module
import hashlib

def hash_file(file):

    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()

    with open(file, 'rb') as f:

        fb = f.read(BLOCK_SIZE)

        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

hash_file(hash_filename)
hash_filesize = os.path.getsize(hash_filename)

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

        self.conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
        logging.info(f"Enviando el archivo {filename} de tamano {filesize}".encode())
        
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            
            while True:

                bytes_read = f.read(BUFFER_SIZE)

                self.conn.send(bytes_read)
                progress.update(len(bytes_read))

                if not bytes_read:
                    break

        logging.info("Se envio correctamente el archivo principal !")
        print("Se envio correctamente el archivo principal !")

        # --> HASH

        self.conn.send(f"{hash_filename}{SEPARATOR}{hash_filesize}".encode())
        logging.info(f"Enviando el archivo {hash_filename} de tamano {hash_filesize}".encode())
        
        progress = tqdm.tqdm(range(hash_filesize), f"Sending {hash_filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(hash_filename, "rb") as f:
            
            while True:

                bytes_read = f.read(BUFFER_SIZE)

                self.conn.send(bytes_read)
                progress.update(len(bytes_read))

                if not bytes_read:
                    break

        logging.info("Se envio correctamente el HASH !")
        print("Se envio correctamente el archivo HASH !")

        self.conn.close()

# --------------------------------------------------------------------------

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <listen>")
    sys.exit(1)
 
HOST, PORT, NUMBER = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind((HOST, PORT))
threads = [] 
 
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