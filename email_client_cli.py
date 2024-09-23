### Email client (CLI)
import os
import readerGmail
import senderGmail
from colorama import Fore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import threading ### Multi hilos
import argparse

### Setting and email login
class LoginEmail:

    def __init__(
        self,
        email_adress = None,
        application_password = None
    ):

        self.email_adress = email_adress
        self.application_password = application_password
        
    ### Encriptador de  claves
    def __encrypt_password(self):
        ### Generar una clave secreta de encriptado y un vector 
        secret_key = os.urandom(16)     ### Clave de 16 bytes para AES-128
        iv = os.urandom(16)             ### Vector de inicialización

        ### Guardar la secrey key y el iv - vector
        with open('auth/.secret_key', 'wb') as secret_key_file:
            secret_key_file.write(secret_key)
        
        with open('auth/.secret_iv', 'wb') as secret_iv_file:
            secret_iv_file.write(iv)


        ### Creacion de un objeto cifrado
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)

        ### Clave para encriptar
        password = self.application_password
        password_bytes = password.encode()

        ### Encriptacion de la clave
        encrypted_password = cipher.encrypt(pad(password_bytes, AES.block_size))

        with open('auth/.password', 'wb') as password_file:
            password_file.write(encrypted_password)

        #### print(f"Texto encriptado: {encrypted_password}")
    

    def __decrypt_password(self):

        with open('auth/.secret_key', 'rb') as secret_key:
            secret_key = secret_key.read()
        
        with open('auth/.secret_iv', 'rb') as secret_iv:
            secret_iv = secret_iv.read()
        
        with open('auth/.password', 'rb') as password_file:
            password = password_file.read()

        ### Leer la clave encriptada
        cipher_dec = AES.new(secret_key, AES.MODE_CBC, secret_iv)
        decrypted_password = unpad(cipher_dec.decrypt(password), AES.block_size)
        decrypted_password = decrypted_password.decode()

        return decrypted_password

    ### Login 
    def login(self):
        
        ### Encriptar las claves del usuario
        self.__encrypt_password()

        ### Iniciar sesion en RaderGmail y SenderGmail
        reader = readerGmail.Getting_email(
            EMAIL = self.email_adress,
            PASSWORD = self.__decrypt_password(),
        )

        sender = senderGmail.SenderEmail(
            email_sender = self.email_adress,
            email_password = self.__decrypt_password()
        )

        tools = [reader, sender]
        return tools


def login():

    print('Email Login -> ')

    username = input("Por favor, Ingrese su correo electronico: ")
    password = input("Por favor, Ingrese su clave de aplicacion: ")

    login = LoginEmail(
        username,
        password
    )

    reader = gmail_tools[0]
    sender = gmail_tools[1]

    print("Login Exitoso, sus credenciales han sido guardadas.")

### (arguemnt - --all) (argument - --only="Email adress")
def read_email(all=True, only=False):

    if all:
        ### Leer todos los mensajes
        pass
    
    elif only:
        ### Read email only one adress
        try:
            email_adress = input('Ingrese el email de quien espera mensaje -> ')
            new_message = reader.wait_email(email_adress)
        except:
            pass
    pass

def write_email():
    try:
        email_receiver = str(input("A quien deseas enviarle el E-mail -> "))
        email = str(input("Ingrese su mensaje: "))

        sender.send(email_receiver, 'default', email)

        

    except:
        pass
    pass


### Make an object for argparse
parser = argparse.ArgumentParser(description='Controles para manejo de email')


# Crear subparsers
subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')


### Test login
parser_a = subparsers.add_parser('login', help='Inicia la session para poder enviar emails')
parser_a.set_defaults(func=login)




# Analizar los argumentos
args = parser.parse_args()

if hasattr(args, 'func'):
    args.func()
else:
    parser.print_help()


### Usar un servidor web flask para una mini interfaz con un arguemnto