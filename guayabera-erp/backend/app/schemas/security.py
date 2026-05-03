from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: str = Field(..., max_length=100, description="Tipo de acción realizada")
    resource_type: str = Field(..., max_length=100, description="Tipo de recurso afectado")
    resource_id: Optional[int] = None
    old_values: Optional[Dict[Any, Any]] = None
    new_values: Optional[Dict[Any, Any]] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    status: str = Field(default="success", max_length=20)
    notes: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class SecurityEventBase(BaseModel):
    user_id: Optional[int] = None
    event_type: str = Field(..., max_length=100, description="Tipo de evento de seguridad")
    severity: str = Field(default="medium", max_length=20)
    description: Optional[str] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    resolved: bool = Field(default=False)
    resolution_notes: Optional[str] = None


class SecurityEventCreate(SecurityEventBase):
    pass


class SecurityEventUpdate(BaseModel):
    resolved: Optional[bool] = None
    resolution_notes: Optional[str] = None


class SecurityEventResponse(SecurityEventBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True