import imaplib
import email

# Conexión al servidor IMAP de Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('moises.p.student@gmail.com', 'pjei qgle dwmo gmpi')

# Seleccionar la bandeja de entrada
mail.select('inbox')

# Buscar correos
result, data = mail.search(None, 'ALL')
email_ids = data[0].split()

# Leer el primer correo
result, msg_data = mail.fetch(email_ids[0], '(RFC822)')
msg = email.message_from_bytes(msg_data[0][1])

# Obtener el asunto y el cuerpo del mensaje
subject = msg['subject']
print("Subject:", subject)

# Si el mensaje es multipart, extraer el cuerpo
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode()
            print("Body:", body)
else:
    body = msg.get_payload(decode=True).decode()
    print("Body:", body)

# Cerrar la conexión
mail.logout()

# ' pjei qgle dwmo gmpi '