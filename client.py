import os
import socket
import ssl

HOST = '127.0.0.1'
PORT = 8080

def create_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

if __name__ == '__main__':
    # Create the SSL client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.load_verify_locations('server.crt')
    context.check_hostname = False
    ssl_sock = context.wrap_socket(sock)

    ssl_sock.connect((HOST, PORT))

    print(ssl_sock.recv(1024).hex())

    ssl_sock.close()