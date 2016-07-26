import socket
import sys

import config
import functions

host = config.host
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else :
    port = config.port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

while True :
    csock, caddr = sock.accept()
    req = csock.recv(1024)

    if req.startswith('POST /addPair') :
        add_thread = functions.addPair(csock, req)
        add_thread.start()
    elif req.startswith('POST /updatePair'):
        update_thread = functions.updatePair(csock, req)
        update_thread.start()
    elif req.startswith('POST /deletePair'):
        delete_thread = functions.deletePair(csock, req)
        delete_thread.start()
    elif req.startswith('GET /view') :
        view_thread = functions.view(csock)
        view_thread.start()
    elif req.startswith('GET /retrieve') :
        retrieve_thread = functions.retrieve(csock, req)
        retrieve_thread.start()
    else :
        csock.sendall("""HTTP/1.0 200 OK
                            Content-Type: text/html\r\n\r\n
                            <html>
                            <head>
                            <title> Invalid </title>
                            </head>
                            <body>
                            The request was not recognised
                            </body>
                            </html>""")
        csock.close()






