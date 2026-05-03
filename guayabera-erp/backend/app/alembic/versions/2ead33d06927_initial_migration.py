"""Initial migration with all essential tables

Revision ID: 2ead33d06927
Revises: 
Create Date: 2026-04-29 21:16:43.777210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision: str = '2ead33d06927'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create extension for UUID if not exists
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    
    # Tablas de seguridad
    op.create_table('seg_usuario',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('is_superuser', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('seg_rol',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(50), nullable=False, unique=True),
        sa.Column('descripcion', sa.String(200)),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('seg_permiso',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(50), nullable=False, unique=True),
        sa.Column('descripcion', sa.String(200)),
        sa.Column('modulo', sa.String(50)),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Tabla intermedia para roles y permisos
    op.create_table('seg_rol_permiso',
        sa.Column('rol_id', UUID(as_uuid=True), sa.ForeignKey('seg_rol.id'), primary_key=True),
        sa.Column('permiso_id', UUID(as_uuid=True), sa.ForeignKey('seg_permiso.id'), primary_key=True)
    )
    
    # Tablas administrativas
    op.create_table('admin_empresa',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('rfc', sa.String(13), unique=True),
        sa.Column('direccion', sa.String(300)),
        sa.Column('telefono', sa.String(20)),
        sa.Column('email', sa.String(100)),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('admin_sucursal',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('empresa_id', UUID(as_uuid=True), sa.ForeignKey('admin_empresa.id'), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('direccion', sa.String(300)),
        sa.Column('telefono', sa.String(20)),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Tablas de contabilidad
    op.create_table('cont_cuenta',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('codigo', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('nivel', sa.Integer, nullable=False),  # 1=grupo, 2=genero, 3=cuenta, 4=subcuenta
        sa.Column('tipo', sa.String(50), nullable=False),  # activo, pasivo, capital, ingresos, costos, gastos
        sa.Column('naturaleza', sa.String(20)),  # deudora, acreedora
        sa.Column('es_cuenta_mayor', sa.Boolean, server_default='false'),
        sa.Column('es_agrupadora', sa.Boolean, server_default='false'),
        sa.Column('numero_cuenta_bancaria', sa.String(20)),
        sa.Column('banco_sat', sa.String(100)),  # Para cuentas bancarias
        sa.Column('activa', sa.Boolean, server_default='true'),
        sa.Column('requiere_centro_costos', sa.Boolean, server_default='false'),
        sa.Column('requiere_documento_referencia', sa.Boolean, server_default='false'),
        sa.Column('descripcion', sa.Text),
        sa.Column('cuenta_padre_id', UUID(as_uuid=True), sa.ForeignKey('cont_cuenta.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_centro_costo',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('codigo', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('descripcion', sa.Text),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_poliza',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('numero', sa.Integer, nullable=False, index=True),
        sa.Column('tipo', sa.String(20), nullable=False),  # diario, ingreso, egreso
        sa.Column('fecha', sa.Date, nullable=False, index=True),
        sa.Column('descripcion', sa.Text, nullable=False),
        sa.Column('comentario_adicional', sa.Text),
        sa.Column('estado', sa.String(20), server_default='borrador'),  # borrador, revisada, aprobada, cancelada
        sa.Column('fecha_aprobacion', sa.DateTime(timezone=True)),
        sa.Column('aprobado_por', UUID(as_uuid=True), sa.ForeignKey('seg_usuario.id')),
        sa.Column('total_cargos', sa.Numeric(15, 2), server_default='0'),
        sa.Column('total_abonos', sa.Numeric(15, 2), server_default='0'),
        sa.Column('esta_cuadrada', sa.Boolean, server_default='false'),
        sa.Column('modulo_origen', sa.String(50)),  # manual, ventas, compras, nomina, produccion
        sa.Column('referencia_externa', sa.String(100)),  # ID del documento origen
        sa.Column('preparado_por', UUID(as_uuid=True), sa.ForeignKey('seg_usuario.id')),
        sa.Column('revisado_por', UUID(as_uuid=True), sa.ForeignKey('seg_usuario.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_poliza_detalle',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('poliza_id', UUID(as_uuid=True), sa.ForeignKey('cont_poliza.id'), nullable=False),
        sa.Column('cuenta_id', UUID(as_uuid=True), sa.ForeignKey('cont_cuenta.id'), nullable=False),
        sa.Column('centro_costo_id', UUID(as_uuid=True), sa.ForeignKey('cont_centro_costo.id')),
        sa.Column('cargo', sa.Numeric(15, 2), server_default='0'),
        sa.Column('abono', sa.Numeric(15, 2), server_default='0'),
        sa.Column('concepto', sa.String(500), nullable=False),
        sa.Column('referencia', sa.String(100)),  # Número de factura, OC, OP, etc.
        sa.Column('documento_referencia', sa.String(100)),  # UUID del documento origen
        sa.Column('fecha_documento', sa.Date),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_banco',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(100), nullable=False),  # BBVA, Banorte, etc.
        sa.Column('cuenta', sa.String(20), unique=True, nullable=False),
        sa.Column('clabe', sa.String(18), unique=True),
        sa.Column('tipo_cuenta', sa.String(50)),  # cheques, ahorro, inversion
        sa.Column('moneda', sa.String(3), server_default='MXN'),
        sa.Column('sucursal', sa.String(100)),
        sa.Column('cuenta_contable_id', UUID(as_uuid=True), sa.ForeignKey('cont_cuenta.id')),
        sa.Column('saldo_actual', sa.Numeric(15, 2), server_default='0'),
        sa.Column('saldo_fecha_corte', sa.Numeric(15, 2), server_default='0'),
        sa.Column('fecha_ultimo_corte', sa.Date),
        sa.Column('activo', sa.Boolean, server_default='true'),
        sa.Column('descripcion', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_movimiento_bancario',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('banco_id', UUID(as_uuid=True), sa.ForeignKey('cont_banco.id'), nullable=False),
        sa.Column('fecha', sa.Date, nullable=False, index=True),
        sa.Column('descripcion', sa.String(500), nullable=False),
        sa.Column('referencia', sa.String(50)),  # Reference number
        sa.Column('tipo_movimiento', sa.String(50)),  # deposito, retiro, transferencia, comision
        sa.Column('cargo', sa.Numeric(15, 2), server_default='0'),
        sa.Column('abono', sa.Numeric(15, 2), server_default='0'),
        sa.Column('saldo', sa.Numeric(15, 2)),
        sa.Column('conciliado', sa.Boolean, server_default='false'),
        sa.Column('fecha_conciliacion', sa.DateTime(timezone=True)),
        sa.Column('poliza_id', UUID(as_uuid=True), sa.ForeignKey('cont_poliza.id')),
        sa.Column('importado', sa.Boolean, server_default='false'),  # Imported from bank file
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_asiento',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('modulo_origen', sa.String(50), nullable=False),  # compras, ventas, nomina, produccion
        sa.Column('entidad_origen', sa.String(100), nullable=False),  # tipo de documento
        sa.Column('entidad_id', UUID(as_uuid=True), nullable=False),
        sa.Column('referencia', sa.String(200)),
        sa.Column('poliza_id', UUID(as_uuid=True), sa.ForeignKey('cont_poliza.id')),
        sa.Column('estado', sa.String(20), server_default='pendiente'),  # pendiente, procesado, cancelado
        sa.Column('fecha_procesado', sa.DateTime(timezone=True)),
        sa.Column('datos_origen', sa.JSON),
        sa.Column('errores', sa.JSON),  # Error details if failed
        sa.Column('creado_por', sa.String(100)),  # System or user
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('cont_periodo',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(50), nullable=False),  # Enero 2025
        sa.Column('fecha_inicio', sa.Date, nullable=False),
        sa.Column('fecha_fin', sa.Date, nullable=False),
        sa.Column('estado', sa.String(20), server_default='abierto'),  # abierto, cerrado, en_cierre
        sa.Column('fecha_cierre', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Agregar las nuevas tablas que creamos para la integración bancaria
    op.create_table('fin_cuenta_bancaria',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('banco', sa.String(100), nullable=False),
        sa.Column('numero_cuenta', sa.String(50), nullable=False, unique=True),
        sa.Column('clabe', sa.String(18), unique=True),
        sa.Column('tipo_cuenta', sa.String(50)),
        sa.Column('moneda', sa.String(3), server_default='MXN'),
        sa.Column('saldo_actual', sa.Numeric(15, 2), server_default='0'),
        sa.Column('saldo_disponible', sa.Numeric(15, 2), server_default='0'),
        sa.Column('cuenta_contable_id', UUID(as_uuid=True), sa.ForeignKey('cont_cuenta.id')),
        sa.Column('activa', sa.Boolean, server_default='true'),
        sa.Column('fecha_alta', sa.Date),
        sa.Column('descripcion', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('fin_transaccion',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('folio', sa.String(50), unique=True),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('sub_tipo', sa.String(50)),
        sa.Column('monto', sa.Numeric(15, 2), nullable=False),
        sa.Column('moneda', sa.String(3), server_default='MXN'),
        sa.Column('tipo_cambio', sa.Numeric(10, 6), server_default='1.0'),
        sa.Column('fecha', sa.Date, nullable=False),
        sa.Column('fecha_valor', sa.Date),
        sa.Column('cuenta_origen_id', UUID(as_uuid=True), sa.ForeignKey('fin_cuenta_bancaria.id')),
        sa.Column('cuenta_destino_id', UUID(as_uuid=True), sa.ForeignKey('fin_cuenta_bancaria.id')),
        sa.Column('poliza_id', UUID(as_uuid=True), sa.ForeignKey('cont_poliza.id')),
        sa.Column('partida_id', UUID(as_uuid=True), sa.ForeignKey('cont_poliza_detalle.id')),
        sa.Column('descripcion', sa.Text, nullable=False),
        sa.Column('referencia', sa.String(100)),
        sa.Column('documento_soporte', sa.String(100)),
        sa.Column('estado', sa.String(20), server_default='registrada'),
        sa.Column('fecha_autorizacion', sa.DateTime(timezone=True)),
        sa.Column('autorizado_por', UUID(as_uuid=True), sa.ForeignKey('seg_usuario.id')),
        sa.Column('creado_por', UUID(as_uuid=True), sa.ForeignKey('seg_usuario.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar tablas en orden inverso al de creación
    op.drop_table('fin_transaccion')
    op.drop_table('fin_cuenta_bancaria')
    op.drop_table('cont_periodo')
    op.drop_table('cont_asiento')
    op.drop_table('cont_movimiento_bancario')
    op.drop_table('cont_banco')
    op.drop_table('cont_poliza_detalle')
    op.drop_table('cont_poliza')
    op.drop_table('cont_centro_costo')
    op.drop_table('cont_cuenta')
    op.drop_table('admin_sucursal')
    op.drop_table('admin_empresa')
    op.drop_table('seg_rol_permiso')
    op.drop_table('seg_permiso')
    op.drop_table('seg_rol')
    op.drop_table('seg_usuario')