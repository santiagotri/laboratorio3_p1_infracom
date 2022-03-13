
# ... https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# ... https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

import sys
import socket
import tqdm
import os

from _thread import *
import threading
 
print_lock = threading.Lock()
BUFFER_SIZE = 4096

filename = "100MB.bin"
filesize = os.path.getsize(filename)
SEPARATOR = "<SEPARATOR>"
 
def threaded(c):

    c.send(f"{filename}{SEPARATOR}{filesize}".encode())

    while True:
 
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            while True:

                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                c.send(bytes_read)
                progress.update(len(bytes_read))
        
        print_lock.release()
        break
 
    c.close()
 
 
def Main():
    
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <host> <port> <listen>")
        sys.exit(1)
 
    HOST, PORT, NUMBER = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
 
    s.listen(NUMBER)
    print(f"Server listening in {HOST} {PORT}")
 
    while True:
 
        c, addr = s.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))
 
 
if __name__ == '__main__':
    Main()