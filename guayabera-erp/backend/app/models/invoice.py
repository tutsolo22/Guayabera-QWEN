"""
Invoice Models: Electronic invoicing according to Mexican SAT regulations
Integration with Facturama for CFDI issuance
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoComprobante(enum.Enum):
    INGRESO = "I"      # Ingreso
    EGRESO = "E"       # Egreso
    TRASLADO = "T"     # Traslado
    NOMINA = "N"       # Nómina
    PAGO = "P"         # Pago


class MetodoPago(enum.Enum):
    PAGO_EN_UNA_EXHIBICION = "PUE"
    PAGO_EN_PARCIALIDADES_DIFERIDO = "PPD"


class FormaPago(enum.Enum):
    EFECTIVO = "01"
    CHEQUE_NOMINATIVO = "02"
    TRANSFERENCIA_ELECTRONICA = "03"
    TARJETA_CREDITO = "04"
    MONEDERO_ELECTRONICO = "05"
    DINERO_ELECTRONICO = "06"
    VALES_DE_DESPENSA = "08"
    DACION_EN_PAGO = "12"
    PAGO_POR_SUBROGACION = "13"
    PAGO_POR_CONSIGNACION = "14"
    CONDONACION = "15"
    COMPENSACION = "17"
    NOVACION = "23"
    CONFUSION = "24"
    REMISION_DE_DEUDA = "25"
    PRESCRIPCION_O_CADUCIDAD = "26"
    A_SATISFACCION_DEL_ACREEDOR = "27"
    TARJETA_DE_DEBITO = "28"
    TARJETA_DE_SERVICIOS = "29"
    APLICACION_DE_ANTICIPOS = "30"
    INTERMEDIARIO_PAGOS = "31"
    POR_DEFINIR = "99"


class UsoCFDI(enum.Enum):
    ADQUISICION_MERCANCIAS = "G01"
    DEVOLUCION_DESCUENTO_BONIFICACION = "G02"
    GASTOS_EN_GENERAL = "G03"
    CONSTRUCCIONES = "I01"
    MOBILIARIO_Y_EQUIPO_DE_OFICINA = "I02"
    EQUIPO_DE_TRANSPORTE = "I03"
    EQUIPO_DE_COMPUTO = "I04"
    HERRAMIENTAS = "I05"
    PROPIEDADES_PLANTA_Y_EQUIPO = "I06"
    OTROS_ACTIVOS_FIJOS = "I07"
    VALORES_Y_ACTIVOS_BIOLÓGICOS = "I08"
    GASTOS_DE_FUNCIÓN = "D01"
    GASTOS_POR_TRASLADOS = "D02"
    PREMIOS = "D03"
    HONORARIOS_MEDICOS_DENTALES_Y_GASTOS_HOSPITALARIOS = "D04"
    GASTOS_FUNERALES = "D05"
    DONATIVOS = "D06"
    INTERESES_POR_CREDITOS_Y_DEUDA = "D07"
    APORTACIONES_Y_PRIMAS_SENDA_SINDICAL = "D08"
    CONCEPTOS_QUE_NO_SE_IMPONEN_IVA = "D09"
    PAGOS_POR_RENTA = "D10"
    PAGOS_POR_DIVIDENDOS = "D11"
    PAGOS_EN_SUSTITUCION_DE_OTROS = "D12"
    PAGOS_POR_SEGUROS = "D13"
    SANCIONES = "D14"
    DEDUCCIONES_SUJETAS_A_TASA_CERO = "D15"
    PAGOS_POR_GASTOS_DEL_TRABAJADOR = "D16"
    COMPRAS_DE_AUTO_USO = "D17"
    GASTOS_POR_SERVICIOS_ADMINISTRATIVOS = "D18"
    OTROS = "P01"


class TipoRelacion(enum.Enum):
    NOTA_CREDITO = "01"
    NOTA_DEBITO = "02"
    DEVOLUCION_MERCANCIA = "03"
    SUSTITUCION_CFDI_PREVIOS = "04"
    TRASLADOS_MERCANCIA_FACTURADOS_PREVIAMENTE = "05"
    FACTURA_POR_TRASLADOS_PENDIENTES = "06"
    FACTURA_GENERADA_POR_PAGOS_EN_PARCIALIDADES = "07"
    FACTURA_GENERADA_POR_ANTICIPOS = "08"


class EstadoComprobante(enum.Enum):
    ACTIVO = "activo"
    CANCELADO = "cancelado"
    ERROR_TIMBRADO = "error_timbrado"
    PENDIENTE_TIMBRADO = "pendiente_timbrado"


class TipoComplemento(enum.Enum):
    PAGO = "pago"
    CARTA_PORTE = "carta_porte"
    NOMINA = "nomina"
    COMERCIO_EXTERIOR = "comercio_exterior"
    DONATARIA = "donataria"
    IEPS = "ieps"
    AEROLINEAS = "aerolineas"
    NOTARIO_PUBLICO = "notario_publico"
    REGIMENES_FISCALES = "regimenes_fiscales"
    SERVICIOS_PLATAFORMAS_TECNOLOGICAS = "servicios_plataformas_tecnologicas"
    INSTITUCIONES_DE_SEGUROS = "instituciones_de_seguros"
    RECICLAJE = "reciclaje"
    COMPRAS = "compras"
    HIDROCARBUROS = "hidrocarburos"
    COORDINADOS = "coordinados"
    TURISTA_PASAJERO_EXTRANJERO = "turista_pasajero_extranjero"
    OOMI = "oomi"
    ACREDITAMIENTO_IEPS = "acreditamiento_ieps"
    VEHICULO_USADO = "vehiculo_usado"
    SERVICIO_CADEMITE = "servicio_cademite"
    INGRESOS_HIPOTECARIOS = "ingresos_hipotecarios"
    PARQUES_Y_ESPACIOS_NATURALES = "parques_y_espacios_naturales"
    PLATAFORMAS_TECNOLOGICAS = "plataformas_tecnologicas"
    CFDI_REGIMEN_FAVORABLE = "cfdi_regimen_favorable"
    COMPLEMENTO_CFDI = "complemento_cfdi"
    COMPLEMENTO_PAGO = "complemento_pago"
    COMPLEMENTO_NOMINA = "complemento_nomina"


# ============================================================================
# INVOICE MODELS
# ============================================================================

class Emisor(Base):
    """Issuer information - Información del emisor"""
    __tablename__ = "inv_emisor"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company identification
    rfc = Column(String(13), unique=True, nullable=False)
    nombre_o_razon_social = Column(String(254), nullable=False)
    regimen_fiscal = Column(String(10), nullable=False)  # SAT catalog code
    
    # Address
    calle = Column(String(100))
    numero_exterior = Column(String(50))
    numero_interior = Column(String(50))
    colonia = Column(String(100))
    localidad = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(50))
    pais = Column(String(50), default="México")
    codigo_postal = Column(String(10))
    
    # Fiscal data
    regimen_fiscal_nombre = Column(String(150))  # Name from SAT catalog
    fac_atencion = Column(String(50))  # Fiscal address code
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Receptor(Base):
    """Receiver information - Información del receptor"""
    __tablename__ = "inv_receptor"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Customer identification
    rfc = Column(String(13), unique=True, nullable=False)
    nombre_o_razon_social = Column(String(254), nullable=False)
    
    # Address
    calle = Column(String(100))
    numero_exterior = Column(String(50))
    numero_interior = Column(String(50))
    colonia = Column(String(100))
    localidad = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(50))
    pais = Column(String(50), default="México")
    codigo_postal = Column(String(10))
    
    # Fiscal data
    regimen_fiscal = Column(String(10))  # SAT catalog code
    uso_cfdi = Column(SQLEnum(UsoCFDI), default=UsoCFDI.ADQUISICION_MERCANCIAS)
    
    # Customer relationship
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"))  # Link to CRM customer
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    cliente = relationship("Cliente")


class ComprobanteFiscal(Base):
    """Fiscal receipt - Comprobante fiscal (CFDI)"""
    __tablename__ = "inv_comprobante_fiscal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document identification
    folio_interno = Column(String(50), unique=True, nullable=False)  # Internal folio
    serie = Column(String(10), default="A")  # Document series
    folio_fiscal = Column(String(36))  # SAT UUID (after stamping)
    
    # Fiscal data
    tipo_comprobante = Column(SQLEnum(TipoComprobante), nullable=False)
    metodo_pago = Column(SQLEnum(MetodoPago), nullable=False)
    forma_pago = Column(SQLEnum(FormaPago), nullable=False)
    uso_cfdi = Column(SQLEnum(UsoCFDI), nullable=False)
    
    # Dates
    fecha_emision = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_certificacion = Column(DateTime(timezone=True))  # When SAT certified
    
    # Amounts
    subtotal = Column(Numeric(12, 2), nullable=False)
    descuento = Column(Numeric(12, 2), default=0.00)
    total_impuestos_retenidos = Column(Numeric(12, 2), default=0.00)
    total_impuestos_trasladados = Column(Numeric(12, 2), default=0.00)
    total = Column(Numeric(12, 2), nullable=False)
    
    # Related documents
    tipo_relacion = Column(SQLEnum(TipoRelacion))
    uuid_relacionados = Column(Text)  # Comma-separated list of related UUIDs
    
    # External IDs
    emisor_id = Column(UUID(as_uuid=True), ForeignKey("inv_emisor.id"), nullable=False)
    receptor_id = Column(UUID(as_uuid=True), ForeignKey("inv_receptor.id"), nullable=False)
    pedido_venta_id = Column(UUID(as_uuid=True), ForeignKey("ventas_pedido.id"))  # Related sale order
    
    # Facturama integration
    facturama_id = Column(String(50))  # ID from Facturama API
    estatus_facturama = Column(String(20))  # Status from Facturama
    estatus_sat = Column(String(20))  # Status from SAT
    cadena_original = Column(Text)  # Original string from SAT
    sello_digital = Column(String(250))  # Digital seal
    sello_sat = Column(String(250))  # SAT seal
    no_certificado = Column(String(20))  # Certificate number
    no_certificado_sat = Column(String(20))  # SAT certificate number
    
    # Status
    estado = Column(SQLEnum(EstadoComprobante), default=EstadoComprobante.PENDIENTE_TIMBRADO)
    
    # Files
    ruta_pdf = Column(String(255))  # Path to PDF file
    ruta_xml = Column(String(255))  # Path to XML file
    
    # Metadata
    condiciones_pago = Column(String(200))
    moneda = Column(String(3), default="MXN")  # Currency
    tipo_cambio = Column(Numeric(10, 6), default=1.000000)  # Exchange rate
    confirmacion = Column(String(6))  # Confirmation number
    observaciones = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    emisor = relationship("Emisor")
    receptor = relationship("Receptor")
    pedido_venta = relationship("PedidoVenta")
    complementos = relationship("ComplementoFiscal", back_populates="comprobante")


class ConceptoFactura(Base):
    """Invoice concept - Concepto de factura"""
    __tablename__ = "inv_concepto_factura"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comprobante_id = Column(UUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"), nullable=False)
    
    # Concept identification
    clave_producto = Column(String(10), nullable=False)  # SAT product code
    clave_unidad = Column(String(10), default="H87")  # SAT unit code (piece)
    no_identificacion = Column(String(100))  # Internal product code
    descripcion = Column(Text, nullable=False)
    
    # Quantities and prices
    cantidad = Column(Numeric(12, 6), nullable=False)
    unidad_medida = Column(String(50), default="Pieza")  # Unit of measurement
    valor_unitario = Column(Numeric(12, 6), nullable=False)
    importe = Column(Numeric(12, 2), nullable=False)
    descuento = Column(Numeric(12, 2), default=0.00)
    
    # Tax data
    objeto_imp = Column(String(2), default="02")  # Tax object: 01=No objeto, 02=Exento, 03=Sujeto
    
    # Related products
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))  # Changed from inv_producto to alm_producto - Link to inventory product
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    comprobante = relationship("ComprobanteFiscal", back_populates="conceptos")
    producto = relationship("Producto")  # Changed from Producto to match correct model


class ImpuestoConcepto(Base):
    """Tax for invoice concept - Impuesto para concepto de factura"""
    __tablename__ = "inv_impuesto_concepto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concepto_id = Column(UUID(as_uuid=True), ForeignKey("inv_concepto_factura.id"), nullable=False)
    
    # Tax identification
    tipo = Column(String(10), nullable=False)  # "Traslado" or "Retencion"
    nombre = Column(String(50), nullable=False)  # Tax name (IVA, ISR)
    tasa_cuota = Column(Numeric(10, 6))  # Rate for traslados
    importe = Column(Numeric(12, 2), nullable=False)  # Amount
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    concepto = relationship("ConceptoFactura", back_populates="impuestos")


class ComplementoPago(Base):
    """Payment complement - Complemento de pago"""
    __tablename__ = "inv_complemento_pago"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comprobante_id = Column(UUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"), nullable=False)
    
    # Payment complement data
    fecha_pago = Column(Date, nullable=False)
    forma_pago = Column(SQLEnum(FormaPago), nullable=False)
    moneda_pago = Column(String(3), default="MXN")
    tipo_cambio_pago = Column(Numeric(10, 6), default=1.000000)
    monto = Column(Numeric(12, 2), nullable=False)
    
    # Bank data
    rfc_emisor_cuenta_ord = Column(String(13))  # RFC of sender account bank
    banco_ordenante_nombre = Column(String(100))  # Name of sender bank
    cuenta_ordenante = Column(String(50))  # Sender account number
    rfc_emisor_cuenta_ben = Column(String(13))  # RFC of recipient account bank
    banco_beneficiario_nombre = Column(String(100))  # Name of recipient bank
    cuenta_beneficiario = Column(String(50))  # Recipient account number
    
    # Related document
    documento_relacionado_id = Column(UUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"))  # Related invoice
    id_documento = Column(String(36), nullable=False)  # UUID of related document
    serie_documento = Column(String(10))
    folio_documento = Column(String(20))
    moneda_dr = Column(String(3), default="MXN")
    tipo_cambio_dr = Column(Numeric(10, 6), default=1.000000)
    metodo_pago_dr = Column(String(10))  # Method from SAT catalog
    num_parcialidad = Column(Integer)  # Partiality number
    saldo_anterior = Column(Numeric(12, 2))  # Previous balance
    importe_pagado = Column(Numeric(12, 2))  # Amount paid
    saldo_insoluto = Column(Numeric(12, 2))  # Outstanding balance
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    comprobante = relationship("ComprobanteFiscal", foreign_keys=[comprobante_id])
    documento_relacionado = relationship("ComprobanteFiscal", foreign_keys=[documento_relacionado_id])


class ComplementoFiscal(Base):
    """Fiscal complement - Complemento fiscal para CFDI"""
    __tablename__ = "inv_complemento_fiscal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comprobante_id = Column(UUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"), nullable=False)
    
    # Complement identification
    tipo_complemento = Column(SQLEnum(TipoComplemento), nullable=False)  # Type of fiscal complement
    nombre = Column(String(100), nullable=False)  # Name of the complement
    descripcion = Column(Text)  # Description of the complement
    
    # Content
    contenido = Column(JSONB)  # Content of the complement in JSON format
    version = Column(String(10))  # Version of the complement
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    comprobante = relationship("ComprobanteFiscal", back_populates="complementos")


class CancelacionCFDI(Base):
    """CFDI cancellation record - Registro de cancelación de CFDI"""
    __tablename__ = "inv_cancelacion_cfdi"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comprobante_id = Column(UUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"), nullable=False)
    
    # Cancellation details
    fecha_cancelacion = Column(DateTime(timezone=True), server_default=func.now())
    motivo_cancelacion = Column(String(200))  # Reason for cancellation
    folio_sustitucion = Column(String(50))  # Substitution folio (for replacements)
    
    # Status
    estado_cancelacion = Column(String(20), default="solicitada")  # solicitada, aceptada, rechazada
    uuid_acuse = Column(String(36))  # UUID of acceptance notice from SAT
    archivo_acuse = Column(String(255))  # Path to acceptance file
    
    # Metadata
    notas = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    comprobante = relationship("ComprobanteFiscal", back_populates="cancelaciones")


class ValidacionRFC(Base):
    """RFC validation record - Registro de validación de RFC"""
    __tablename__ = "inv_validacion_rfc"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfc = Column(String(13), unique=True, nullable=False, index=True)  # RFC for validation
    
    # Validation results
    nombre_razon_social = Column(String(250))
    fecha_validacion = Column(DateTime(timezone=True), server_default=func.now())
    estatus_general = Column(String(50))  # Active, cancelled, etc.
    estatus_contribuyente = Column(String(50))
    regimen_fiscal = Column(String(100))
    codigo_postal = Column(String(10))
    
    # Blacklist status
    en_lista_negra = Column(Boolean, default=False)
    motivo_lista_negra = Column(Text)
    
    # Validation metadata
    fuente_datos = Column(String(100))  # Source of validation data
    ultima_verificacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    comprobante_emitidos = relationship("ComprobanteFiscal", foreign_keys="ComprobanteFiscal.emisor_id")
    comprobante_recibidos = relationship("ComprobanteFiscal", foreign_keys="ComprobanteFiscal.receptor_id")


# Add relationships to ComprobanteFiscal
ComprobanteFiscal.conceptos = relationship("ConceptoFactura", back_populates="comprobante")
ConceptoFactura.impuestos = relationship("ImpuestoConcepto", back_populates="concepto")
ComprobanteFiscal.cancelaciones = relationship("CancelacionCFDI", back_populates="comprobante")
