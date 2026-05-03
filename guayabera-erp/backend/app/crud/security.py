from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.security import AuditLog, SecurityEvent
from app.schemas.security import AuditLogCreate, AuditLogUpdate, AuditLogResponse, SecurityEventCreate, SecurityEventUpdate, SecurityEventResponse


# CRUD para AuditLog
def create_audit_log(db: Session, audit_log: AuditLogCreate) -> AuditLog:
    db_audit_log = AuditLog(**audit_log.model_dump())
    db.add(db_audit_log)
    db.commit()
    db.refresh(db_audit_log)
    return db_audit_log


def get_audit_log(db: Session, audit_log_id: int) -> Optional[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()


def get_audit_logs(db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()


def get_audit_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return (
        db.query(AuditLog)
        .filter(AuditLog.user_id == user_id)
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_audit_logs_by_resource(db: Session, resource_type: str, resource_id: int) -> List[AuditLog]:
    return (
        db.query(AuditLog)
        .filter(AuditLog.resource_type == resource_type, AuditLog.resource_id == resource_id)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )


def update_audit_log(db: Session, audit_log_id: int, audit_log_update: AuditLogUpdate) -> Optional[AuditLog]:
    db_audit_log = db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()
    if db_audit_log:
        update_data = audit_log_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_audit_log, field, value)
        db.commit()
        db.refresh(db_audit_log)
    return db_audit_log


def delete_audit_log(db: Session, audit_log_id: int) -> bool:
    db_audit_log = db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()
    if db_audit_log:
        db.delete(db_audit_log)
        db.commit()
        return True
    return False


# CRUD para SecurityEvent
def create_security_event(db: Session, security_event: SecurityEventCreate) -> SecurityEvent:
    db_security_event = SecurityEvent(**security_event.model_dump())
    db.add(db_security_event)
    db.commit()
    db.refresh(db_security_event)
    return db_security_event


def get_security_event(db: Session, security_event_id: int) -> Optional[SecurityEvent]:
    return db.query(SecurityEvent).filter(SecurityEvent.id == security_event_id).first()


def get_security_events(db: Session, skip: int = 0, limit: int = 100) -> List[SecurityEvent]:
    return db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).offset(skip).limit(limit).all()


def get_security_events_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[SecurityEvent]:
    return (
        db.query(SecurityEvent)
        .filter(SecurityEvent.user_id == user_id)
        .order_by(SecurityEvent.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_security_events_by_type(db: Session, event_type: str, skip: int = 0, limit: int = 100) -> List[SecurityEvent]:
    return (
        db.query(SecurityEvent)
        .filter(SecurityEvent.event_type == event_type)
        .order_by(SecurityEvent.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_unresolved_security_events(db: Session) -> List[SecurityEvent]:
    return (
        db.query(SecurityEvent)
        .filter(SecurityEvent.resolved == False)
        .order_by(SecurityEvent.timestamp.desc())
        .all()
    )


def update_security_event(
    db: Session, security_event_id: int, security_event_update: SecurityEventUpdate
) -> Optional[SecurityEvent]:
    db_security_event = db.query(SecurityEvent).filter(SecurityEvent.id == security_event_id).first()
    if db_security_event:
        update_data = security_event_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_security_event, field, value)
        db.commit()
        db.refresh(db_security_event)
    return db_security_event


def delete_security_event(db: Session, security_event_id: int) -> bool:
    db_security_event = db.query(SecurityEvent).filter(SecurityEvent.id == security_event_id).first()
    if db_security_event:
        db.delete(db_security_event)
        db.commit()
        return True
    return False