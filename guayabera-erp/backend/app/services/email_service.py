"""
Email Service: SMTP settings for sending invoices, quotes, etc.
Integrated with company configuration and includes test functionality
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import logging
from cryptography.fernet import Fernet

from app.models.email_config import ConfiguracionCorreo

# Configure logging
logger = logging.getLogger(__name__)


class EmailService:
    """
    Service class to handle email sending operations
    Uses SMTP configuration from the database
    """
    
    def __init__(self, config: ConfiguracionCorreo):
        """
        Initialize email service with configuration
        :param config: Email configuration from database
        """
        self.config = config
        
        # Decrypt password
        from app.core.config import settings
        f = Fernet(settings.SECRET_KEY.encode()[:44] + b'=')
        self.password = f.decrypt(config.contrasena_smtp.encode()).decode()
    
    def send_email(
        self,
        destinatarios: List[str],
        asunto: str,
        cuerpo: str,
        copia: Optional[List[str]] = None,
        copia_oculta: Optional[List[str]] = None,
        adjuntos: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email using the configured SMTP settings
        :param destinatarios: List of recipient email addresses
        :param asunto: Subject of the email
        :param cuerpo: Body of the email
        :param copia: List of CC email addresses
        :param copia_oculta: List of BCC email addresses
        :param adjuntos: List of file paths to attach
        :return: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.config.nombre_remitente} <{self.config.correo_remitente}>" if self.config.nombre_remitente else self.config.correo_remitente
            msg['To'] = ", ".join(destinatarios)
            msg['Subject'] = asunto
            
            if copia:
                msg['Cc'] = ", ".join(copia)
            
            # Add body to email
            msg.attach(MIMEText(cuerpo, 'html'))
            
            # Add attachments if any
            if adjuntos:
                for file_path in adjuntos:
                    self._add_attachment(msg, file_path)
            
            # Combine all recipients
            all_recipients = destinatarios[:]
            if copia:
                all_recipients.extend(copia)
            if copia_oculta:
                all_recipients.extend(copia_oculta)
            
            # Create SMTP session
            context = ssl.create_default_context()
            
            if self.config.seguridad_smtp.lower() == "ssl":
                server = smtplib.SMTP_SSL(self.config.servidor_smtp, self.config.puerto_smtp, context=context)
            else:
                server = smtplib.SMTP(self.config.servidor_smtp, self.config.puerto_smtp)
                if self.config.seguridad_smtp.lower() == "tls":
                    server.starttls(context=context)
            
            # Login and send email
            server.login(self.config.usuario_smtp, self.password)
            text = msg.as_string()
            server.sendmail(self.config.correo_remitente, all_recipients, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {len(all_recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """
        Add an attachment to the email message
        :param msg: The email message object
        :param file_path: Path to the file to attach
        """
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Extract filename from path
            filename = file_path.split('/')[-1].split('\\')[-1]
            part.add_header(
                'Content-Disposition',
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
        except Exception as e:
            logger.error(f"Failed to attach file {file_path}: {str(e)}")
    
    def test_connection(self, destinatario_prueba: str) -> dict:
        """
        Test the email configuration by sending a test email
        :param destinatario_prueba: Email address to send the test to
        :return: Dictionary with test result
        """
        try:
            # Create a simple test message
            asunto = "Prueba de Configuración de Correo - GuayaberaERP"
            cuerpo = f"""
            <html>
              <body>
                <h2>Prueba de Configuración de Correo</h2>
                <p>Esta es una prueba para verificar la configuración de correo electrónico.</p>
                <p>Si recibió este mensaje, su configuración SMTP es correcta.</p>
                <br>
                <p>Detalles de la configuración:</p>
                <ul>
                  <li>Servidor SMTP: {self.config.servidor_smtp}</li>
                  <li>Puerto: {self.config.puerto_smtp}</li>
                  <li>Seguridad: {self.config.seguridad_smtp}</li>
                  <li>Remitente: {self.config.correo_remitente}</li>
                </ul>
                <br>
                <p>Fecha de prueba: {self._get_current_datetime()}</p>
              </body>
            </html>
            """
            
            success = self.send_email(
                destinatarios=[destinatario_prueba],
                asunto=asunto,
                cuerpo=cuerpo
            )
            
            if success:
                return {
                    "status": "success",
                    "message": "Configuración de correo verificada exitosamente"
                }
            else:
                return {
                    "status": "error",
                    "message": "Falló el envío del correo de prueba"
                }
                
        except Exception as e:
            logger.error(f"Test connection failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Error al conectar con el servidor SMTP: {str(e)}"
            }
    
    def _get_current_datetime(self):
        """Get current datetime as string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")