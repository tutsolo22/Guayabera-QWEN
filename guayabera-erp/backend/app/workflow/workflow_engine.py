"""
Workflow Engine: Implements workflow and hierarchical approval systems
Manages business processes and approval chains
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base
from app.models import Usuario


class ApprovalStatus(Enum):
    """Status of approval requests"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class WorkflowAction(Enum):
    """Possible workflow actions"""
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"
    COMPLETE = "complete"


class ApprovalRequest(Base):
    """Approval request entity"""
    __tablename__ = "wf_approval_request"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Request details
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo = Column(String(100), nullable=False)  # purchase_order, expense_claim, etc.
    entidad_id = Column(String(100), nullable=False)  # ID of the entity being approved
    entidad_tipo = Column(String(100), nullable=False)  # Type of the entity
    
    # Status and flow
    estado = Column(String(20), default=ApprovalStatus.PENDING.value)
    nivel_actual = Column(Integer, default=1)  # Current approval level
    nivel_maximo = Column(Integer, default=1)  # Max approval level needed
    
    # Users involved
    solicitante_id = Column(PostgresUUID(as_uuid=True), ForeignKey("auth_usuario.id"), nullable=False)
    aprobador_actual_id = Column(PostgresUUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # Current approver
    aprobadores_secuencia = Column(Text)  # JSON array of user IDs in approval sequence
    
    # Business data
    datos_adicionales = Column(Text)  # JSON with additional business data
    
    # Dates
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_vencimiento = Column(DateTime(timezone=True))  # When the request expires
    fecha_aprobacion = Column(DateTime(timezone=True))  # When approved
    
    # Relationships
    solicitante = relationship("Usuario", foreign_keys=[solicitante_id])
    aprobador_actual = relationship("Usuario", foreign_keys=[aprobador_actual_id])


class WorkflowLog(Base):
    """Log of workflow actions"""
    __tablename__ = "wf_log"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference to approval request
    solicitud_id = Column(PostgresUUID(as_uuid=True), ForeignKey("wf_approval_request.id"), nullable=False)
    
    # Action details
    accion = Column(String(50), nullable=False)  # approve, reject, escalate, etc.
    comentario = Column(Text)
    
    # Actor details
    usuario_id = Column(PostgresUUID(as_uuid=True), ForeignKey("auth_usuario.id"), nullable=False)
    usuario_nombre = Column(String(200))
    
    # Context
    nivel = Column(Integer)  # Approval level when action occurred
    estado_anterior = Column(String(20))
    estado_nuevo = Column(String(20))
    
    # Timestamp
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    solicitud = relationship("ApprovalRequest")
    usuario = relationship("Usuario")


class WorkflowEngine:
    """
    Main workflow engine to manage business processes
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.approvers_by_level = {}  # Map of approval levels to user IDs
        self.workflow_rules = {}  # Business rules for different entities
    
    def create_approval_request(
        self,
        titulo: str,
        descripcion: str,
        tipo: str,
        entidad_id: str,
        entidad_tipo: str,
        solicitante_id: UUID,
        aprobadores: List[UUID],
        datos_adicionales: Optional[Dict[str, Any]] = None,
        fecha_vencimiento: Optional[datetime] = None
    ) -> ApprovalRequest:
        """
        Create a new approval request
        :param titulo: Title of the request
        :param descripcion: Description of the request
        :param tipo: Type of request (purchase_order, expense_claim, etc.)
        :param entidad_id: ID of the entity being approved
        :param entidad_tipo: Type of the entity
        :param solicitante_id: ID of the requesting user
        :param aprobadores: List of user IDs in approval sequence
        :param datos_adicionales: Additional business data
        :param fecha_vencimiento: Expiration date for the request
        :return: Created ApprovalRequest object
        """
        import json
        
        request = ApprovalRequest(
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            entidad_id=entidad_id,
            entidad_tipo=entidad_tipo,
            nivel_maximo=len(aprobadores),
            solicitante_id=solicitante_id,
            aprobadores_secuencia=json.dumps([str(uid) for uid in aprobadores]),
            datos_adicionales=json.dumps(datos_adicionales) if datos_adicionales else None,
            fecha_vencimiento=fecha_vencimiento
        )
        
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        
        # Set first approver
        self.set_next_approver(request)
        
        # Log the submission
        self.log_action(
            solicitud_id=request.id,
            accion=WorkflowAction.SUBMIT.value,
            usuario_id=solicitante_id,
            comentario="Solicitud creada y enviada para aprobación",
            nivel=request.nivel_actual,
            estado_anterior=ApprovalStatus.PENDING.value,
            estado_nuevo=ApprovalStatus.PENDING.value
        )
        
        return request
    
    def approve_request(self, solicitud_id: UUID, usuario_id: UUID, comentario: str = None) -> ApprovalRequest:
        """
        Approve an approval request
        :param solicitud_id: ID of the request to approve
        :param usuario_id: ID of the approving user
        :param comentario: Optional comment
        :return: Updated ApprovalRequest object
        """
        solicitud = self.get_request(solicitud_id)
        if not solicitud:
            raise ValueError(f"Solicitud con ID {solicitud_id} no encontrada")
        
        if solicitud.estado != ApprovalStatus.PENDING.value:
            raise ValueError(f"Solicitud no está pendiente, estado actual: {solicitud.estado}")
        
        # Verify this user is the current approver
        if solicitud.aprobador_actual_id != usuario_id:
            raise ValueError("Usuario no autorizado para aprobar esta solicitud")
        
        # Move to next level or approve completely
        if solicitud.nivel_actual >= solicitud.nivel_maximo:
            # Final approval
            solicitud.estado = ApprovalStatus.APPROVED.value
            solicitud.fecha_aprobacion = datetime.utcnow()
            estado_nuevo = ApprovalStatus.APPROVED.value
        else:
            # Move to next level
            solicitud.nivel_actual += 1
            self.set_next_approver(solicitud)
            estado_nuevo = ApprovalStatus.PENDING.value
        
        self.db.commit()
        self.db.refresh(solicitud)
        
        # Log the approval action
        self.log_action(
            solicitud_id=solicitud.id,
            accion=WorkflowAction.APPROVE.value,
            usuario_id=usuario_id,
            comentario=comentario or "Solicitud aprobada",
            nivel=solicitud.nivel_actual - 1 if solicitud.estado == ApprovalStatus.PENDING.value else solicitud.nivel_actual,
            estado_anterior=ApprovalStatus.PENDING.value,
            estado_nuevo=estado_nuevo
        )
        
        return solicitud
    
    def reject_request(self, solicitud_id: UUID, usuario_id: UUID, comentario: str = None) -> ApprovalRequest:
        """
        Reject an approval request
        :param solicitud_id: ID of the request to reject
        :param usuario_id: ID of the rejecting user
        :param comentario: Optional comment
        :return: Updated ApprovalRequest object
        """
        solicitud = self.get_request(solicitud_id)
        if not solicitud:
            raise ValueError(f"Solicitud con ID {solicitud_id} no encontrada")
        
        if solicitud.estado != ApprovalStatus.PENDING.value:
            raise ValueError(f"Solicitud no está pendiente, estado actual: {solicitud.estado}")
        
        # Verify this user is the current approver
        if solicitud.aprobador_actual_id != usuario_id:
            raise ValueError("Usuario no autorizado para rechazar esta solicitud")
        
        solicitud.estado = ApprovalStatus.REJECTED.value
        solicitud.nivel_actual = solicitud.nivel_maximo  # Set to max to indicate completion
        
        self.db.commit()
        self.db.refresh(solicitud)
        
        # Log the rejection action
        self.log_action(
            solicitud_id=solicitud.id,
            accion=WorkflowAction.REJECT.value,
            usuario_id=usuario_id,
            comentario=comentario or "Solicitud rechazada",
            nivel=solicitud.nivel_actual,
            estado_anterior=ApprovalStatus.PENDING.value,
            estado_nuevo=ApprovalStatus.REJECTED.value
        )
        
        return solicitud
    
    def get_request(self, solicitud_id: UUID) -> Optional[ApprovalRequest]:
        """
        Get an approval request by ID
        :param solicitud_id: ID of the request
        :return: ApprovalRequest object or None
        """
        return self.db.query(ApprovalRequest).filter(ApprovalRequest.id == solicitud_id).first()
    
    def get_requests_by_user(
        self, 
        usuario_id: UUID, 
        estados: List[str] = None, 
        tipo: str = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[ApprovalRequest]:
        """
        Get approval requests for a user
        :param usuario_id: ID of the user
        :param estados: List of states to filter by
        :param tipo: Type of requests to filter by
        :param skip: Number of records to skip
        :param limit: Maximum number of records to return
        :return: List of ApprovalRequest objects
        """
        query = self.db.query(ApprovalRequest).filter(
            (ApprovalRequest.solicitante_id == usuario_id) | 
            (ApprovalRequest.aprobador_actual_id == usuario_id)
        )
        
        if estados:
            query = query.filter(ApprovalRequest.estado.in_(estados))
        
        if tipo:
            query = query.filter(ApprovalRequest.tipo == tipo)
        
        return query.offset(skip).limit(limit).all()
    
    def get_pending_requests_for_user(self, usuario_id: UUID) -> List[ApprovalRequest]:
        """
        Get all pending requests assigned to a user
        :param usuario_id: ID of the user
        :return: List of pending ApprovalRequest objects
        """
        return self.db.query(ApprovalRequest).filter(
            ApprovalRequest.aprobador_actual_id == usuario_id,
            ApprovalRequest.estado == ApprovalStatus.PENDING.value
        ).all()
    
    def set_next_approver(self, solicitud: ApprovalRequest):
        """
        Set the next approver in the sequence
        :param solicitud: ApprovalRequest object to update
        """
        import json
        
        aprobadores_seq = json.loads(solicitud.aprobadores_secuencia)
        
        # Get the user ID at the current level (0-indexed)
        if solicitud.nivel_actual <= len(aprobadores_seq):
            next_approver_id = UUID(aprobadores_seq[solicitud.nivel_actual - 1])
            solicitud.aprobador_actual_id = next_approver_id
    
    def log_action(
        self, 
        solicitud_id: UUID, 
        accion: str, 
        usuario_id: UUID, 
        comentario: str = None,
        nivel: int = None,
        estado_anterior: str = None,
        estado_nuevo: str = None
    ):
        """
        Log a workflow action
        :param solicitud_id: ID of the related request
        :param accion: Action taken
        :param usuario_id: ID of the user who took the action
        :param comentario: Optional comment
        :param nivel: Approval level
        :param estado_anterior: Previous state
        :param estado_nuevo: New state
        """
        # Get user name for the log
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        usuario_nombre = f"{usuario.nombre} {usuario.apellidos}" if usuario else "Usuario desconocido"
        
        log_entry = WorkflowLog(
            solicitud_id=solicitud_id,
            accion=accion,
            comentario=comentario,
            usuario_id=usuario_id,
            usuario_nombre=usuario_nombre,
            nivel=nivel,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo
        )
        
        self.db.add(log_entry)
        self.db.commit()
    
    def get_workflow_history(self, solicitud_id: UUID) -> List[WorkflowLog]:
        """
        Get the history of actions for a request
        :param solicitud_id: ID of the request
        :return: List of WorkflowLog objects
        """
        return self.db.query(WorkflowLog).filter(
            WorkflowLog.solicitud_id == solicitud_id
        ).order_by(WorkflowLog.fecha_registro).all()
    
    def escalate_request(self, solicitud_id: UUID, usuario_id: UUID, comentario: str = None) -> ApprovalRequest:
        """
        Escalate a request to a higher authority
        :param solicitud_id: ID of the request to escalate
        :param usuario_id: ID of the user escalating
        :param comentario: Optional comment
        :return: Updated ApprovalRequest object
        """
        solicitud = self.get_request(solicitud_id)
        if not solicitud:
            raise ValueError(f"Solicitud con ID {solicitud_id} no encontrada")
        
        # Increase approval level by 1, but not beyond the max
        if solicitud.nivel_actual < solicitud.nivel_maximo:
            solicitud.nivel_actual += 1
            self.set_next_approver(solicitud)
        
        self.db.commit()
        self.db.refresh(solicitud)
        
        # Log the escalation
        self.log_action(
            solicitud_id=solicitud.id,
            accion=WorkflowAction.ESCALATE.value,
            usuario_id=usuario_id,
            comentario=comentario or "Solicitud escalada a siguiente nivel",
            nivel=solicitud.nivel_actual,
            estado_anterior=solicitud.estado,
            estado_nuevo=solicitud.estado
        )
        
        return solicitud


def get_workflow_engine(db: Session) -> WorkflowEngine:
    """
    Factory function to create a workflow engine instance
    :param db: Database session
    :return: WorkflowEngine instance
    """
    return WorkflowEngine(db)