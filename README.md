# Trojen-Ransomeware



### Overview
This project demonstrates a simple ransomware attack and recovery mechanism using Python, SSL/TLS for secure communication, and AES encryption. It consists of a server and a client that communicate over a secure channel. The client encrypts files in a target directory, and the server can later release the decryption key to restore the files.

---

### Project Structure

```
Trojan-Ransomeware/
│
├── client.py         # The ransomware client (attacker)    | Visible
├── server.py         # The key management server           | Visible
├── server.crt        # SSL certificate (self-signed)       | Hidden
├── server.key        # SSL private key                     | Hidden
└── README.md         # Project documentation               | Visible
```

---

### How It Works

1. **Server (`server.py`)**
    - Listens for incoming SSL connections.
    - Generates a random AES key for each client (by IP) and saves it in `keys/`.
    - Sends the key to the client for encryption.
    - Waits for manual input (`release`) to send the key again, allowing the client to decrypt files.

2. **Client (`client.py`)**
    - Connects to the server over SSL.
    - Receives the AES key and encrypts all files in the `files/` directory using AES-CBC.
    - Waits for the server to send the key again, then decrypts the files.

---

### Usage

1. **Generate SSL Certificates**
	 - You need `server.crt` and `server.key` in the project root. You can generate them using OpenSSL:
		 ```sh
		 openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
		 ```

2. **Start the Server**
	 - Run the server in one terminal:
		 ```sh
		 python server.py
		 ```

3. **Start the Client**
    - In another terminal / your target PC, run:
        ```sh
        python client.py
        ```

4. **Release the Key**
	 - On the server terminal, type `release` and press Enter to allow the client to decrypt the files.

---

### Requirements
- Python 3.x
- `pycryptodome` (for AES):
	```sh
	pip install pycryptodome
	```

---

### Security & Ethical Notice
- This code is for educational and research purposes only.
- Do **not** use this code to attack or compromise any system without explicit permission.

