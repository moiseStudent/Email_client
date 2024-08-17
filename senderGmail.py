### Script para enviar mensajes por email 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SenderEmail:

    def __init__(self, email_sender, email_password):
        
        self.email_sender = email_sender
        self.email_password = email_password

    
    
    def __email_settings(self):

        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.msg = MIMEMultipart()
        self.msg['From'] = self.email_sender
        self.msg['To'] = self.email_receiver
        self.msg['Subject'] = self.subject

        ### Adjuntar el cuerpo del mensaje
        self.msg.attach(MIMEText(self.body, 'plain'))
    
    def __send_email(self):
        ### Send Email
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(self.msg)
            return 'Correo enviado exitosamente.'
        
        except Exception as e:
            return f'Ocurrió un error: {e}'
        
        finally:
            server.quit()
    
    def send(
        self,
        email_receiver,
        subject,
        body
        ):
            self.email_receiver = email_receiver
            self.subject = subject
            self.body = body
            self.__email_settings()
            print(self.__send_email())