"""
Multi-Factor Authentication: Implements MFA for enhanced security
Provides TOTP and SMS-based authentication options
"""

import pyotp
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy.orm import Session
from app.models.security import Usuario, MetodoMFA, SesionMFA
from app.core.config import settings
from app.security.compliance import ComplianceMeasures


class MFAType(Enum):
    """Enumeration of MFA types"""
    TOTP = "totp"           # Time-based One-Time Password
    SMS = "sms"             # SMS-based authentication
    EMAIL = "email"         # Email-based authentication
    BACKUP_CODE = "backup"  # Backup codes


class MFAManager:
    """
    Manager class for Multi-Factor Authentication
    """
    
    def __init__(self):
        self.compliance = ComplianceMeasures()
    
    def generate_totp_secret(self) -> str:
        """
        Generate a secret key for TOTP
        :return: Base32 encoded secret key
        """
        return pyotp.random_base32()
    
    def generate_qr_code(self, secret: str, username: str, issuer: str = "GuayaberaERP") -> str:
        """
        Generate QR code for TOTP setup
        :param secret: Secret key for TOTP
        :param username: Username to associate with the TOTP
        :param issuer: Name of the service
        :return: Base64 encoded QR code image
        """
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()
        
        # Encode to base64
        img_base64 = base64.b64encode(img_bytes).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    def verify_totp_token(self, secret: str, token: str, window: int = 1) -> bool:
        """
        Verify a TOTP token
        :param secret: Secret key used to generate tokens
        :param token: Token to verify
        :param window: Window of time steps to allow
        :return: True if valid, False otherwise
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=window)
    
    def send_sms_code(self, phone_number: str, code: str) -> bool:
        """
        Send SMS code to user (placeholder implementation)
        :param phone_number: Phone number to send to
        :param code: Code to send
        :return: True if sent successfully
        """
        # In a real implementation, integrate with an SMS service like Twilio
        print(f"SMS code {code} sent to {phone_number}")
        return True  # Placeholder return value
    
    def send_email_code(self, email: str, code: str, username: str) -> bool:
        """
        Send email code to user
        :param email: Email address to send to
        :param code: Code to send
        :param username: Username for personalization
        :return: True if sent successfully
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_SENDER
            msg['To'] = email
            msg['Subject'] = "Código de Autenticación de Dos Factores - GuayaberaERP"
            
            body = f"""
            Hola {username},
            
            Tu código de autenticación de dos factores para GuayaberaERP es: {code}
            
            Este código expira en 10 minutos.
            
            Si no solicitaste este código, por favor ignora este mensaje.
            
            Saludos,
            Equipo de GuayaberaERP
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # In a real implementation, use actual SMTP settings
            # For now, just simulate the send
            print(f"Email code {code} sent to {email}")
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def generate_backup_codes(self, count: int = 10) -> list:
        """
        Generate backup codes for MFA recovery
        :param count: Number of codes to generate
        :return: List of backup codes
        """
        import secrets
        codes = []
        
        for _ in range(count):
            # Generate a 16-character alphanumeric code
            code = secrets.token_urlsafe(12)[:16].upper().replace('_', '').replace('-', '')
            codes.append(code)
        
        return codes
    
    def enable_mfa_method(
        self, 
        db: Session, 
        user_id: str, 
        mfa_type: MFAType, 
        secret: str = None,
        phone_number: str = None,
        email: str = None
    ) -> MetodoMFA:
        """
        Enable an MFA method for a user
        :param db: Database session
        :param user_id: ID of the user
        :param mfa_type: Type of MFA to enable
        :param secret: Secret key for TOTP (if applicable)
        :param phone_number: Phone number for SMS (if applicable)
        :param email: Email address for email-based MFA (if applicable)
        :return: Created MetodoMFA object
        """
        # Check if user already has this MFA type enabled
        existing_method = db.query(MetodoMFA).filter(
            MetodoMFA.usuario_id == user_id,
            MetodoMFA.tipo == mfa_type.value,
            MetodoMFA.activado == True
        ).first()
        
        if existing_method:
            # Disable existing method first
            existing_method.activado = False
            existing_method.fecha_desactivacion = datetime.utcnow()
            db.commit()
        
        # Create new MFA method
        mfa_method = MetodoMFA(
            usuario_id=user_id,
            tipo=mfa_type.value,
            activado=True,
            secreto=secret,
            telefono=phone_number,
            email=email,
            fecha_activacion=datetime.utcnow()
        )
        
        db.add(mfa_method)
        db.commit()
        db.refresh(mfa_method)
        
        # Generate backup codes if this is the first MFA method
        user_methods = db.query(MetodoMFA).filter(
            MetodoMFA.usuario_id == user_id,
            MetodoMFA.activado == True
        ).count()
        
        if user_methods == 1:
            self.generate_and_store_backup_codes(db, user_id)
        
        return mfa_method
    
    def generate_and_store_backup_codes(self, db: Session, user_id: str):
        """
        Generate and store backup codes for a user
        :param db: Database session
        :param user_id: ID of the user
        """
        backup_codes = self.generate_backup_codes()
        
        for code in backup_codes:
            hashed_code = self.compliance.generate_secure_hash(code)
            backup_mfa = MetodoMFA(
                usuario_id=user_id,
                tipo=MFAType.BACKUP_CODE.value,
                activado=True,
                secreto=hashed_code,
                fecha_activacion=datetime.utcnow()
            )
            db.add(backup_mfa)
        
        db.commit()
    
    def authenticate_with_mfa(
        self, 
        db: Session, 
        user_id: str, 
        mfa_type: MFAType, 
        token: str
    ) -> bool:
        """
        Authenticate user with MFA
        :param db: Database session
        :param user_id: ID of the user
        :param mfa_type: Type of MFA being used
        :param token: Token provided by user
        :return: True if authentication successful
        """
        mfa_method = db.query(MetodoMFA).filter(
            MetodoMFA.usuario_id == user_id,
            MetodoMFA.tipo == mfa_type.value,
            MetodoMFA.activado == True
        ).first()
        
        if not mfa_method:
            return False
        
        if mfa_type == MFAType.TOTP:
            return self.verify_totp_token(mfa_method.secreto, token)
        elif mfa_type == MFAType.BACKUP_CODE:
            # Verify backup code
            for backup_method in db.query(MetodoMFA).filter(
                MetodoMFA.usuario_id == user_id,
                MetodoMFA.tipo == MFAType.BACKUP_CODE.value,
                MetodoMFA.activado == True
            ).all():
                if self.compliance.verify_hash(token, backup_method.secreto):
                    # Mark this backup code as used (deactivate it)
                    backup_method.activado = False
                    backup_method.fecha_desactivacion = datetime.utcnow()
                    db.commit()
                    return True
            return False
        else:
            # For SMS and EMAIL, we would need to implement a verification store
            # This is a simplified implementation
            print(f"Verification of {mfa_type} not fully implemented in this example")
            return False
    
    def create_mfa_session(
        self, 
        db: Session, 
        user_id: str, 
        session_id: str, 
        expires_in: int = 300  # 5 minutes
    ) -> SesionMFA:
        """
        Create an MFA session record
        :param db: Database session
        :param user_id: ID of the user
        :param session_id: Session identifier
        :param expires_in: Seconds until expiration
        :return: Created SesionMFA object
        """
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        mfa_session = SesionMFA(
            usuario_id=user_id,
            sesion_id=session_id,
            activa=True,
            fecha_expiracion=expires_at
        )
        
        db.add(mfa_session)
        db.commit()
        db.refresh(mfa_session)
        
        return mfa_session
    
    def validate_mfa_session(self, db: Session, session_id: str) -> bool:
        """
        Validate an MFA session
        :param db: Database session
        :param session_id: Session identifier to validate
        :return: True if session is valid and active
        """
        mfa_session = db.query(SesionMFA).filter(
            SesionMFA.sesion_id == session_id,
            SesionMFA.activa == True
        ).first()
        
        if not mfa_session:
            return False
        
        # Check if session has expired
        if mfa_session.fecha_expiracion < datetime.utcnow():
            # Mark as inactive
            mfa_session.activa = False
            db.commit()
            return False
        
        return True
    
    def disable_mfa_method(self, db: Session, method_id: str) -> bool:
        """
        Disable an MFA method
        :param db: Database session
        :param method_id: ID of the MFA method to disable
        :return: True if successful
        """
        mfa_method = db.query(MetodoMFA).filter(
            MetodoMFA.id == method_id
        ).first()
        
        if mfa_method:
            mfa_method.activado = False
            mfa_method.fecha_desactivacion = datetime.utcnow()
            db.commit()
            return True
        
        return False
    
    def get_user_mfa_methods(self, db: Session, user_id: str) -> list:
        """
        Get all active MFA methods for a user
        :param db: Database session
        :param user_id: ID of the user
        :return: List of active MFA methods
        """
        return db.query(MetodoMFA).filter(
            MetodoMFA.usuario_id == user_id,
            MetodoMFA.activado == True
        ).all()


# Initialize MFA manager
mfa_manager = MFAManager()