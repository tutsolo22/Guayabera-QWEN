"""
Notification Service: Generate notifications based on system events
Specialized for ERP system notifications
"""

from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.notifications import create_notificacion
from app.schemas.notifications import NotificacionCreate
from app.models.notifications import TipoNotificacion, PrioridadNotificacion, CanalNotificacion


def crear_notificacion_pedido_almacen(
    db: Session,
    solicitante_id: UUID,
    supervisor_id: UUID,
    producto_nombre: str,
    cantidad: float,
    unidad: str,
    departamento_solicitante_nombre: str
):
    """
    Crear notificación cuando un departamento solicita productos de almacén
    """
    # Notificación para el supervisor del solicitante
    notificacion_supervisor = NotificacionCreate(
        titulo=f"Solicitud de {producto_nombre} pendiente de autorización",
        descripcion=f"El empleado del departamento {departamento_solicitante_nombre} ha solicitado {cantidad} {unidad} de {producto_nombre}. Se requiere su autorización.",
        tipo=TipoNotificacion.AUTORIZACION.value,
        prioridad=PrioridadNotificacion.ALTA.value,
        canal=CanalNotificacion.INTERNO.value,
        destinatario_id=supervisor_id,
        remitente_id=solicitante_id,
        requiere_confirmacion=True,
        tipo_relacion="pedido_almacen",
        datos_adicionales={
            "solicitante_id": str(solicitante_id),
            "producto_nombre": producto_nombre,
            "cantidad": cantidad,
            "unidad": unidad
        }
    )
    create_notificacion(db, notificacion_supervisor)

    # Notificación para el encargado de almacén
    # Buscar al encargado del almacén
    from app.models.hr import Empleado
    almacen_manager = db.query(Empleado).filter(
        Empleado.puesto.ilike("%almacén%") | 
        Empleado.puesto.ilike("%almacen%") |
        Empleado.puesto.ilike("%inventario%")
    ).first()

    if almacen_manager:
        notificacion_almacen = NotificacionCreate(
            titulo=f"Nueva solicitud de {producto_nombre}",
            descripcion=f"El departamento {departamento_solicitante_nombre} ha solicitado {cantidad} {unidad} de {producto_nombre}. Pendiente de revisión y autorización.",
            tipo=TipoNotificacion.SOLICITUD.value,
            prioridad=PrioridadNotificacion.NORMAL.value,
            canal=CanalNotificacion.INTERNO.value,
            destinatario_id=almacen_manager.id,
            remitente_id=solicitante_id,
            requiere_confirmacion=True,
            tipo_relacion="pedido_almacen",
            datos_adicionales={
                "solicitante_id": str(solicitante_id),
                "producto_nombre": producto_nombre,
                "cantidad": cantidad,
                "unidad": unidad
            }
        )
        create_notificacion(db, notificacion_almacen)


def crear_notificacion_ticket_asignado(
    db: Session,
    ticket_id: UUID,
    ticket_folio: str,
    asignado_a_id: UUID,
    solicitante_nombre: str,
    titulo_ticket: str
):
    """
    Crear notificación cuando se asigna un ticket a un técnico
    """
    notificacion = NotificacionCreate(
        titulo=f"Nuevo ticket asignado: {ticket_folio}",
        descripcion=f"Se te ha asignado el ticket #{ticket_folio} '{titulo_ticket}' solicitado por {solicitante_nombre}.",
        tipo=TipoNotificacion.TAREA.value,
        prioridad=PrioridadNotificacion.NORMAL.value,
        canal=CanalNotificacion.INTERNO.value,
        destinatario_id=asignado_a_id,
        requiere_confirmacion=True,
        tipo_relacion="ticket",
        id_relacion=ticket_id,
        datos_adicionales={
            "ticket_folio": ticket_folio,
            "solicitante_nombre": solicitante_nombre,
            "titulo_ticket": titulo_ticket
        }
    )
    create_notificacion(db, notificacion)


def crear_notificacion_requisicion_aprobada(
    db: Session,
    requisicion_codigo: str,
    solicitante_id: UUID,
    aprobador_nombre: str,
    tipo_requisicion: str
):
    """
    Crear notificación cuando se aprueba una requisición
    """
    notificacion = NotificacionCreate(
        titulo=f"Requisición {requisicion_codigo} aprobada",
        descripcion=f"Tu requisición de {tipo_requisicion} ha sido aprobada por {aprobador_nombre}.",
        tipo=TipoNotificacion.AVISO.value,
        prioridad=PrioridadNotificacion.NORMAL.value,
        canal=CanalNotificacion.INTERNO.value,
        destinatario_id=solicitante_id,
        requiere_confirmacion=False,
        tipo_relacion="requisicion",
        datos_adicionales={
            "requisicion_codigo": requisicion_codigo,
            "aprobador_nombre": aprobador_nombre,
            "tipo_requisicion": tipo_requisicion
        }
    )
    create_notificacion(db, notificacion)


def crear_notificacion_producto_agotado(
    db: Session,
    producto_nombre: str,
    stock_actual: float,
    minimo_stock: float
):
    """
    Crear notificación cuando un producto alcanza nivel mínimo de stock
    """
    # Buscar al responsable de compras
    from app.models.hr import Empleado
    responsable_compras = db.query(Empleado).filter(
        Empleado.puesto.ilike("%compras%") | 
        Empleado.puesto.ilike("%adquisiciones%")
    ).first()

    if responsable_compras:
        notificacion = NotificacionCreate(
            titulo=f"Producto {producto_nombre} bajo en stock",
            descripcion=f"El producto '{producto_nombre}' tiene solo {stock_actual} unidades disponibles, por debajo del mínimo de {minimo_stock}.",
            tipo=TipoNotificacion.ALERTA.value,
            prioridad=PrioridadNotificacion.ALTA.value,
            canal=CanalNotificacion.INTERNO.value,
            destinatario_id=responsable_compras.id,
            requiere_confirmacion=True,
            tipo_relacion="producto",
            datos_adicionales={
                "producto_nombre": producto_nombre,
                "stock_actual": stock_actual,
                "minimo_stock": minimo_stock
            }
        )
        create_notificacion(db, notificacion)


def crear_notificacion_cotizacion_seleccionada(
    db: Session,
    requisicion_codigo: str,
    proveedor_nombre: str,
    solicitante_id: UUID,
    total_cotizacion: float
):
    """
    Crear notificación cuando se selecciona una cotización para una requisición
    """
    notificacion = NotificacionCreate(
        titulo=f"Cotización seleccionada para {requisicion_codigo}",
        descripcion=f"Se ha seleccionado la cotización del proveedor {proveedor_nombre} con un total de ${total_cotizacion}. Se requiere tu autorización para proceder con la orden de compra.",
        tipo=TipoNotificacion.AUTORIZACION.value,
        prioridad=PrioridadNotificacion.ALTA.value,
        canal=CanalNotificacion.INTERNO.value,
        destinatario_id=solicitante_id,
        requiere_confirmacion=True,
        tipo_relacion="cotizacion",
        datos_adicionales={
            "requisicion_codigo": requisicion_codigo,
            "proveedor_nombre": proveedor_nombre,
            "total_cotizacion": total_cotizacion
        }
    )
    create_notificacion(db, notificacion)