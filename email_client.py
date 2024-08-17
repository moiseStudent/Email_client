### Email client 
import os
import readerGmail
import senderGmail
from colorama import Fore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import threading ### Multi hilos

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


### User Interface
def user_interface():

    print(f"\t{Fore.RED}.:|Email Client V1|:.{Fore.RESET}")
    print()
    print("""
1. LOGIN EMAIL - si no esta logeado
2. INICIAR CHAT
3. USAR SERVIDOR WEB LOCAL - (no disponible)
4. SALIR
    """)

### Menu option
while True:

    ### User Interface:
    user_interface()
    option = input("Ingrese una opcion -> ")

    if option == '1':
        print('Login')

        username = input("Por favor, Ingrese su correo electronico: ")
        password = input("Por favor, Ingrese su clave de aplicacion: ")

        login = LoginEmail(
            username,
            password
        )

        gmail_tools = login.login()

        reader = gmail_tools[0]
        sender = gmail_tools[1]
        print("Sus credenciales han sido guardadas.")
    
    elif option == '2':
        email_wait = input("Ingrese el email de quien espera mensaje: ")

        def daemon_read_email():
            while True:
                time.sleep(10) ### Esperar 10 s entre cada verificacion
                new_email = reader.wait_email(email_wait)
        
        ### Thread - Hilo para leer mensajes
        hilo_mensajes = threading.Thread(target=daemon_read_email)
         ### Permite que el hilo se cierre cuando el programa principal termina
        hilo_mensajes.daemon = True
        hilo_mensajes.start()

        while True:

            sms = None

            if sms == None:
                sms = input("\nMensaje: ")
                sender.send(email_wait, 'default', sms)
                
            elif sms != None:
                sms = None
    
    elif option == '3':
        exit()
    
    else:
        print("Wey!!, Opcion no disponible.")