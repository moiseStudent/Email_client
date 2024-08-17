import imaplib
import email
import time
from colorama import Fore
from playsound import playsound


class Getting_email:

    def __init__(self,EMAIL,PASSWORD):

        self.EMAIL = EMAIL
        self.PASSWORD = PASSWORD
        self.MAIL_SERVER = 'imap.gmail.com'
        
    ### Revisar ultimo email
    def check_email(self):

        # Conexión al servidor IMAP de Gmail
        self.mail = imaplib.IMAP4_SSL(self.MAIL_SERVER)
        self.mail.login(self.EMAIL, self.PASSWORD)
        self.mail.select('inbox')

        # Buscar correos no leídos
        result, data = self.mail.search(None, 'UNSEEN')
        email_ids = data[0].split()

        for email_id in email_ids:
            result, msg_data = self.mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Verificar si el remitente coincide con el esperado
            if msg['from'] == self.REMITENTE_ESPERADO:
                subject = msg['subject']
                decoration = '-'
                print(f'\n{Fore.BLUE}{decoration * 50 }{Fore.RESET}')
                print("Nuevo mensaje recibido de:", msg['from'])
                print("Subject:", subject)
                playsound('sounds/livechat-129007.mp3') ### Sonido
                

                # Si el mensaje es multipart, extraer el cuerpo
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print("Body:", body)
                else:
                    body = msg.get_payload(decode=True).decode()
                    print("Body:", body)
                
                return True
            

        # Cerrar la conexión
        self.mail.logout()
    
    def wait_email(self,REMITENTE_ESPERADO):

        self.REMITENTE_ESPERADO = REMITENTE_ESPERADO

        if self.check_email() != None:
            return True
        
        else:
            return False