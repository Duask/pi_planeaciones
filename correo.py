import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario, enlace_restablecimiento):
    # Configuración del servidor SMTP
    servidor_smtp = "smtp.gmail.com"  # Cambia esto si utilizas un proveedor de correo diferente
    puerto_smtp = 587  # Puerto de SMTP

    # Información de autenticación
    remitente = "tu_correo@gmail.com"  # Tu dirección de correo electrónico
    contraseña = "tu_contraseña"  # Tu contraseña de correo electrónico

    # Crear el objeto de mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "Restablecimiento de contraseña"

    # Cuerpo del mensaje
    cuerpo_mensaje = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {enlace_restablecimiento}"
    mensaje.attach(MIMEText(cuerpo_mensaje, "plain"))

    # Conexión y envío del correo electrónico
    with smtplib.SMTP(server=servidor_smtp, port=puerto_smtp) as servidor:
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.send_message(mensaje)

    print("El correo electrónico ha sido enviado exitosamente.")

# Ejemplo de uso
destinatario = "saenzu147@gmail.com"  # Correo electrónico del destinatario
enlace = "https://example.com/restablecer_contraseña"  # Enlace de restablecimiento de contraseña

enviar_correo(destinatario, enlace)
