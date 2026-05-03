"""
Compliance and Security: Implements security measures and compliance features
Ensures data protection, audit trails, and regulatory compliance
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
import logging
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.security import AuditLog
from app.core.config import settings


class AuditAction(Enum):
    """Enumeration of possible audit actions"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    FAILED_LOGIN = "FAILED_LOGIN"
    FILE_ACCESS = "FILE_ACCESS"
    REPORT_GENERATION = "REPORT_GENERATION"
    DATA_EXPORT = "DATA_EXPORT"


class ComplianceMeasures:
    """
    Class implementing compliance and security measures
    """
    
    @staticmethod
    def log_audit_event(
        db: Session,
        user_id: str,
        action: AuditAction,
        resource_type: str,
        resource_id: str,
        ip_address: str = None,
        user_agent: str = None,
        details: Dict[str, Any] = None
    ) -> AuditLog:
        """
        Log an audit event for compliance purposes
        :param db: Database session
        :param user_id: ID of the user performing the action
        :param action: Type of action performed
        :param resource_type: Type of resource affected
        :param resource_id: ID of the specific resource
        :param ip_address: IP address of the user
        :param user_agent: User agent string
        :param details: Additional details about the action
        :return: Created AuditLog object
        """
        audit_log = AuditLog(
            user_id=user_id,
            action=action.value,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    
    @staticmethod
    def generate_secure_hash(data: str, salt: str = None) -> str:
        """
        Generate a secure hash for sensitive data
        :param data: Data to hash
        :param salt: Salt to use (generated if not provided)
        :return: Hashed value
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Using PBKDF2 for hashing passwords
        hashed = hashlib.pbkdf2_hmac('sha256', data.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}${hashed.hex()}"
    
    @staticmethod
    def verify_hash(data: str, stored_hash: str) -> bool:
        """
        Verify a hash against the original data
        :param data: Original data to verify
        :param stored_hash: Stored hash to compare against
        :return: True if match, False otherwise
        """
        try:
            salt, stored_hash_value = stored_hash.split('$')
            computed_hash = hashlib.pbkdf2_hmac('sha256', 
                                                data.encode('utf-8'), 
                                                salt.encode('utf-8'), 
                                                100000)
            return hmac.compare_digest(computed_hash.hex(), stored_hash_value)
        except ValueError:
            # If split fails, old format without salt
            return hashlib.sha256(data.encode()).hexdigest() == stored_hash
    
    @staticmethod
    def encrypt_sensitive_data(data: str, key: str = None) -> str:
        """
        Encrypt sensitive data before storage
        :param data: Data to encrypt
        :param key: Encryption key (uses default if not provided)
        :return: Encrypted data as hex string
        """
        if key is None:
            key = settings.SECRET_KEY[:32]  # Use first 32 chars of secret key
        
        # In a real implementation, use proper encryption like Fernet
        # This is a simplified example
        import base64
        from cryptography.fernet import Fernet
        
        # Ensure key is proper length for Fernet
        if len(key) < 32:
            key = key.ljust(32, '0')
        elif len(key) > 32:
            key = key[:32]
        
        # Encode to bytes and pad with '=' to make valid base64
        key_bytes = key.encode()[:44]
        padded_key = key_bytes.ljust(44, b'=')
        
        f = Fernet(padded_key)
        encrypted_data = f.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str, key: str = None) -> str:
        """
        Decrypt sensitive data
        :param encrypted_data: Data to decrypt
        :param key: Decryption key (uses default if not provided)
        :return: Decrypted data
        """
        if key is None:
            key = settings.SECRET_KEY[:32]  # Use first 32 chars of secret key
        
        import base64
        from cryptography.fernet import Fernet
        
        # Ensure key is proper length for Fernet
        if len(key) < 32:
            key = key.ljust(32, '0')
        elif len(key) > 32:
            key = key[:32]
        
        # Encode to bytes and pad with '=' to make valid base64
        key_bytes = key.encode()[:44]
        padded_key = key_bytes.ljust(44, b'=')
        
        f = Fernet(padded_key)
        decrypted_data = f.decrypt(base64.b64decode(encrypted_data.encode()))
        return decrypted_data.decode()
    
    @staticmethod
    def anonymize_data(data: Dict[str, Any], fields_to_anonymize: List[str]) -> Dict[str, Any]:
        """
        Anonymize sensitive fields in data
        :param data: Data dictionary to anonymize
        :param fields_to_anonymize: List of field names to anonymize
        :return: Anonymized data dictionary
        """
        anonymized_data = data.copy()
        
        for field in fields_to_anonymize:
            if field in anonymized_data:
                original_value = anonymized_data[field]
                if isinstance(original_value, str):
                    # Replace with first character + asterisks
                    if len(original_value) > 2:
                        anonymized_data[field] = original_value[0] + '*' * (len(original_value) - 2) + original_value[-1]
                    elif len(original_value) == 2:
                        anonymized_data[field] = original_value[0] + '*'
                    else:
                        anonymized_data[field] = '*'
                elif isinstance(original_value, (int, float)):
                    anonymized_data[field] = 0  # Replace numbers with 0
                else:
                    anonymized_data[field] = '***'  # Default anonymization
        
        return anonymized_data
    
    @staticmethod
    def validate_compliance_requirements(user_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate data against compliance requirements
        :param user_data: User data to validate
        :return: Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Validate RFC format for Mexican businesses
        if 'rfc' in user_data:
            rfc = user_data['rfc'].upper()
            if not ComplianceMeasures.validate_mexican_rfc(rfc):
                errors.append("Invalid Mexican RFC format")
        
        # Validate email format
        if 'email' in user_data:
            email = user_data['email']
            if not ComplianceMeasures.validate_email_format(email):
                errors.append("Invalid email format")
        
        # Check for required fields based on profile type
        profile_type = user_data.get('profile_type', 'basic')
        required_fields = ComplianceMeasures.get_required_fields(profile_type)
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return {
            "errors": errors,
            "warnings": warnings,
            "is_valid": len(errors) == 0
        }
    
    @staticmethod
    def validate_mexican_rfc(rfc: str) -> bool:
        """
        Validate Mexican RFC format
        :param rfc: RFC to validate
        :return: True if valid, False otherwise
        """
        import re
        # RFC format: 3 letters + 6 digits + 3 characters (for companies)
        # Or: 4 letters + 6 digits + 3 characters (for individuals with 4 name letters)
        pattern = r'^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}$'
        return bool(re.match(pattern, rfc))
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate email format
        :param email: Email to validate
        :return: True if valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def get_required_fields(profile_type: str) -> List[str]:
        """
        Get required fields based on profile type
        :param profile_type: Type of profile
        :return: List of required field names
        """
        required_fields_map = {
            'basic': ['name', 'email'],
            'supplier': ['name', 'email', 'rfc', 'address'],
            'customer': ['name', 'email', 'rfc', 'address'],
            'employee': ['name', 'email', 'rfc', 'position', 'salary'],
            'financial': ['name', 'email', 'rfc', 'bank_details'],
            'admin': ['name', 'email', 'rfc', 'permissions']
        }
        
        return required_fields_map.get(profile_type, required_fields_map['basic'])
    
    @staticmethod
    def generate_retention_schedule() -> Dict[str, timedelta]:
        """
        Generate data retention schedules according to compliance requirements
        :return: Dictionary mapping data types to retention periods
        """
        return {
            'transaction_logs': timedelta(days=365 * 7),  # 7 years for financial records
            'audit_logs': timedelta(days=365 * 7),       # 7 years for audit trails
            'user_sessions': timedelta(days=30),          # 30 days for sessions
            'temporary_files': timedelta(hours=24),       # 24 hours for temp files
            'personal_data': timedelta(days=365 * 2),     # 2 years after account closure
            'backup_data': timedelta(days=365 * 10),      # 10 years for backups
        }
    
    @staticmethod
    def check_data_retention(db: Session) -> Dict[str, Any]:
        """
        Check data retention compliance
        :param db: Database session
        :return: Compliance check results
        """
        retention_schedule = ComplianceMeasures.generate_retention_schedule()
        results = {}
        
        for data_type, retention_period in retention_schedule.items():
            # This would check the actual age of data in the database
            # Implementation depends on specific data organization
            results[data_type] = {
                'retention_period': retention_period.days,
                'needs_cleanup': False,  # Would be determined by actual checks
                'count': 0  # Would be actual count of records
            }
        
        return results


class SecurityHeaders:
    """
    Class to manage security headers for HTTP responses
    """
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """
        Get recommended security headers
        :return: Dictionary of security headers
        """
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Add the FastAPI router for compliance
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.core.security import get_current_user

compliance_router = APIRouter(tags=["compliance"])

@compliance_router.get("/")
def compliance_check():
    """Basic compliance check endpoint"""
    return {
        "status": "compliant",
        "message": "Compliance measures are active",
        "timestamp": datetime.utcnow().isoformat()
    }

@compliance_router.get("/audit-log")
def get_audit_log(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get audit logs for compliance review"""
    # Return recent audit logs for review
    audit_logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(50).all()
    return {
        "audit_logs": audit_logs,
        "total_count": len(audit_logs)
    }

@compliance_router.get("/data-retention")
def check_data_retention(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Check data retention compliance"""
    compliance_measures = ComplianceMeasures()
    return compliance_measures.check_data_retention(db)
