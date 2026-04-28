from .admin import *
from .security import *
from .finance import *
from .supply_chain import *
from .production import *
from .hr import *
from .sales import *
from .inventory import *
from .cad import *
from .size_chart import *
from .helpdesk import *
from .requisitions import *
from .notifications import *
from .quality_control import *
from .advanced_accounting import *
from .logistics import *
from .crm import *
from .project_management import *
from .asset_management import *
from .business_intelligence import *
from .invoice import *
from .email_config import *
from .payroll import *
from .agents import *

__all__ = [
    # Admin CRUD
    "create_empresa", "get_empresa", "get_empresas", "update_empresa", "delete_empresa",
    "create_sucursal", "get_sucursal", "get_sucursales", "update_sucursal", "delete_sucursal",
    "get_configuracion", "set_configuracion", "get_config_by_clave",
    "create_moneda", "get_moneda", "get_monedas",
    "create_impuesto", "get_impuesto", "get_impuestos",
    
    # Security CRUD
    "create_usuario", "get_usuario", "get_usuarios", "update_usuario", "delete_usuario", "authenticate_usuario",
    "create_rol", "get_rol", "get_roles", "update_rol", "delete_rol",
    "create_permiso", "get_permiso", "get_permisos", "update_permiso", "delete_permiso",
    "create_auditoria", "get_auditoria", "get_auditoria_by_usuario", "get_auditoria_by_fecha",
    
    # Finance CRUD
    "create_cuenta_contable", "get_cuenta_contable", "get_cuentas_contables", "update_cuenta_contable", "delete_cuenta_contable",
    "create_centro_costo", "get_centro_costo", "get_centros_costo", "update_centro_costo", "delete_centro_costo",
    "create_poliza_contable", "get_poliza_contable", "get_polizas_contables", "update_poliza_contable", "delete_poliza_contable",
    "create_movimiento_poliza", "get_movimiento_poliza", "get_movimientos_poliza", "update_movimiento_poliza", "delete_movimiento_poliza",
    "create_banco", "get_banco", "get_bancos", "update_banco", "delete_banco",
    "create_movimiento_bancario", "get_movimiento_bancario", "get_movimientos_bancarios", "update_movimiento_bancario", "delete_movimiento_bancario",
    "create_asiento_contable", "get_asiento_contable", "get_asientos_contables", "update_asiento_contable", "delete_asiento_contable",
    "create_periodo_contable", "get_periodo_contable", "get_periodos_contables", "update_periodo_contable", "delete_periodo_contable",
    
    # Supply Chain CRUD
    "create_proveedor", "get_proveedor", "get_proveedores", "update_proveedor", "delete_proveedor",
    "create_contrato_proveedor", "get_contrato_proveedor", "get_contratos_proveedor", "update_contrato_proveedor", "delete_contrato_proveedor",
    "create_orden_compra", "get_orden_compra", "get_ordenes_compra", "update_orden_compra", "delete_orden_compra",
    "create_detalle_orden_compra", "get_detalle_orden_compra", "get_detalles_orden_compra", "update_detalle_orden_compra", "delete_detalle_orden_compra",
    
    # Production CRUD
    "create_producto_textil", "get_producto_textil", "get_productos_textiles", "update_producto_textil", "delete_producto_textil",
    "create_receta_produccion", "get_receta_produccion", "get_recetas_produccion", "update_receta_produccion", "delete_receta_produccion",
    "create_lista_materiales", "get_lista_materiales", "get_listas_materiales", "update_lista_materiales", "delete_lista_materiales",
    "create_ficha_tecnica", "get_ficha_tecnica", "get_fichas_tecnicas", "update_ficha_tecnica", "delete_ficha_tecnica",
    "create_control_calidad", "get_control_calidad", "get_controles_calidad", "update_control_calidad", "delete_control_calidad",
    
    # HR CRUD
    "create_empleado", "get_empleado", "get_empleados", "update_empleado", "delete_empleado",
    "create_departamento", "get_departamento", "get_departamentos", "update_departamento", "delete_departamento",
    "create_puesto", "get_puesto", "get_puestos", "update_puesto", "delete_puesto",
    "create_contrato", "get_contrato", "get_contratos", "update_contrato", "delete_contrato",
    
    # Sales CRUD
    "create_cliente", "get_cliente", "get_clientes", "update_cliente", "delete_cliente",
    "create_contacto_cliente", "get_contacto_cliente", "get_contactos_cliente", "update_contacto_cliente", "delete_contacto_cliente",
    "create_oportunidad_venta", "get_oportunidad_venta", "get_oportunidades_venta", "update_oportunidad_venta", "delete_oportunidad_venta",
    "create_pedido", "get_pedido", "get_pedidos", "update_pedido", "delete_pedido",
    "create_detalle_pedido", "get_detalle_pedido", "get_detalles_pedido", "update_detalle_pedido", "delete_detalle_pedido",
    "create_cotizacion", "get_cotizacion", "get_cotizaciones", "update_cotizacion", "delete_cotizacion",
    "create_detalle_cotizacion", "get_detalle_cotizacion", "get_detalles_cotizacion", "update_detalle_cotizacion", "delete_detalle_cotizacion",
    "create_precio_cliente", "get_precio_cliente", "get_precios_cliente", "update_precio_cliente", "delete_precio_cliente",
    
    # Inventory CRUD
    "create_producto", "get_producto", "get_productos", "update_producto", "delete_producto",
    "create_movimiento_inventario", "get_movimiento_inventario", "get_movimientos_inventario", "update_movimiento_inventario", "delete_movimiento_inventario",
    "create_ubicacion_almacen", "get_ubicacion_almacen", "get_ubicaciones_almacen", "update_ubicacion_almacen", "delete_ubicacion_almacen",
    "create_lote", "get_lote", "get_lotes", "update_lote", "delete_lote",
    
    # CAD CRUD
    "create_diseno_producto", "get_diseno_producto", "get_disenos_producto", "update_diseno_producto", "delete_diseno_producto",
    "create_patron", "get_patron", "get_patrones", "update_patron", "delete_patron",
    "create_biblioteca_patron", "get_biblioteca_patron", "get_bibliotecas_patron", "update_biblioteca_patron", "delete_biblioteca_patron",
    "create_hoja_talla", "get_hoja_talla", "get_hojas_talla", "update_hoja_talla", "delete_hoja_talla",
    
    # Size Chart CRUD
    "create_sistema_talla", "get_sistema_talla", "get_sistemas_talla", "update_sistema_talla", "delete_sistema_talla",
    "create_grupo_talla", "get_grupo_talla", "get_grupos_talla", "update_grupo_talla", "delete_grupo_talla",
    "create_relacion_talla", "get_relacion_talla", "get_relaciones_talla", "update_relacion_talla", "delete_relacion_talla",
    
    # Helpdesk CRUD
    "create_ticket", "get_ticket", "get_tickets", "update_ticket", "delete_ticket",
    "create_categoria_ticket", "get_categoria_ticket", "get_categorias_ticket", "update_categoria_ticket", "delete_categoria_ticket",
    "create_respuesta_ticket", "get_respuesta_ticket", "get_respuestas_ticket", "update_respuesta_ticket", "delete_respuesta_ticket",
    
    # Requisitions CRUD
    "create_solicitud_material", "get_solicitud_material", "get_solicitudes_material", "update_solicitud_material", "delete_solicitud_material",
    "create_detalle_solicitud", "get_detalle_solicitud", "get_detalles_solicitud", "update_detalle_solicitud", "delete_detalle_solicitud",
    
    # Notifications CRUD
    "create_notificacion", "get_notificacion", "get_notificaciones", "update_notificacion", "delete_notificacion",
    "create_canal_notificacion", "get_canal_notificacion", "get_canales_notificacion", "update_canal_notificacion", "delete_canal_notificacion",
    "create_preferencia_notificacion", "get_preferencia_notificacion", "get_preferencias_notificacion", "update_preferencia_notificacion", "delete_preferencia_notificacion",
    
    # Quality Control CRUD
    "create_procedimiento_control", "get_procedimiento_control", "get_procedimientos_control", "update_procedimiento_control", "delete_procedimiento_control",
    "create_incidencia_calidad", "get_incidencia_calidad", "get_incidencias_calidad", "update_incidencia_calidad", "delete_incidencia_calidad",
    "create_certificacion_producto", "get_certificacion_producto", "get_certificaciones_producto", "update_certificacion_producto", "delete_certificacion_producto",
    
    # Advanced Accounting CRUD
    "create_conciliacion", "get_conciliacion", "get_conciliaciones", "update_conciliacion", "delete_conciliacion",
    "create_distribucion_costo", "get_distribucion_costo", "get_distribuciones_costo", "update_distribucion_costo", "delete_distribucion_costo",
    "create_centro_beneficio", "get_centro_beneficio", "get_centros_beneficio", "update_centro_beneficio", "delete_centro_beneficio",
    
    # Logistics CRUD
    "create_proveedor_logistica", "get_proveedor_logistica", "get_proveedores_logistica", "update_proveedor_logistica", "delete_proveedor_logistica",
    "create_tarifa_logistica", "get_tarifa_logistica", "get_tarifas_logistica", "update_tarifa_logistica", "delete_tarifa_logistica",
    "create_ruta_distribucion", "get_ruta_distribucion", "get_rutas_distribucion", "update_ruta_distribucion", "delete_ruta_distribucion",
    "create_ubicacion_geografica", "get_ubicacion_geografica", "get_ubicaciones_geograficas", "update_ubicacion_geografica", "delete_ubicacion_geografica",
    
    # CRM CRUD
    "create_lead", "get_lead", "get_leads", "update_lead", "delete_lead",
    "create_campania_marketing", "get_campania_marketing", "get_campanias_marketing", "update_campania_marketing", "delete_campania_marketing",
    "create_seguimiento_cliente", "get_seguimiento_cliente", "get_seguimientos_cliente", "update_seguimiento_cliente", "delete_seguimiento_cliente",
    
    # Project Management CRUD
    "create_proyecto", "get_proyecto", "get_proyectos", "update_proyecto", "delete_proyecto",
    "create_tarea_proyecto", "get_tarea_proyecto", "get_tareas_proyecto", "update_tarea_proyecto", "delete_tarea_proyecto",
    "create_recurso_proyecto", "get_recurso_proyecto", "get_recursos_proyecto", "update_recurso_proyecto", "delete_recurso_proyecto",
    
    # Asset Management CRUD
    "create_activo_fijo", "get_activo_fijo", "get_activos_fijos", "update_activo_fijo", "delete_activo_fijo",
    "create_depreciacion", "get_depreciacion", "get_depreciaciones", "update_depreciacion", "delete_depreciacion",
    "create_mantenimiento_activo", "get_mantenimiento_activo", "get_mantenimientos_activo", "update_mantenimiento_activo", "delete_mantenimiento_activo",
    
    # Business Intelligence CRUD
    "create_reporte", "get_reporte", "get_reportes", "update_reporte", "delete_reporte",
    "create_indicador_kpi", "get_indicador_kpi", "get_indicadores_kpi", "update_indicador_kpi", "delete_indicador_kpi",
    "create_tablero_control", "get_tablero_control", "get_tableros_control", "update_tablero_control", "delete_tablero_control",
    
    # Invoice CRUD
    "create_emisor", "get_emisor", "get_emisores", "update_emisor", "delete_emisor",
    "create_receptor", "get_receptor", "get_receptores", "update_receptor", "delete_receptor",
    "create_comprobante_fiscal", "get_comprobante_fiscal", "get_comprobantes_fiscales", "update_comprobante_fiscal", "delete_comprobante_fiscal",
    "create_concepto_fiscal", "get_concepto_fiscal", "get_conceptos_fiscales", "update_concepto_fiscal", "delete_concepto_fiscal",
    "create_impuesto_concepto", "get_impuesto_concepto", "get_impuestos_concepto", "update_impuesto_concepto", "delete_impuesto_concepto",
    "create_relacion_cfdi", "get_relacion_cfdi", "get_relaciones_cfdi", "update_relacion_cfdi", "delete_relacion_cfdi",
    "create_configuracion_facturama", "get_configuracion_facturama", "update_configuracion_facturama", "delete_configuracion_facturama",
    "create_registro_facturama", "get_registro_facturama", "get_registros_facturama", "update_registro_facturama", "delete_registro_facturama",
    "create_complemento_pago", "get_complemento_pago", "get_complementos_pago", "update_complemento_pago", "delete_complemento_pago",
    "create_complemento_carta_porte", "get_complemento_carta_porte", "get_complementos_carta_porte", "update_complemento_carta_porte", "delete_complemento_carta_porte",
    "create_complemento_nominas", "get_complemento_nominas", "get_complementos_nominas", "update_complemento_nominas", "delete_complemento_nominas",
    "create_complemento_comercio_exterior", "get_complemento_comercio_exterior", "get_complementos_comercio_exterior", "update_complemento_comercio_exterior", "delete_complemento_comercio_exterior",
    "create_cancelacion_cfdi", "get_cancelacion_cfdi", "get_cancelaciones_cfdi", "update_cancelacion_cfdi", "delete_cancelacion_cfdi",
    "create_validacion_rfc", "get_validacion_rfc", "get_validaciones_rfc", "update_validacion_rfc", "delete_validacion_rfc",
    
    # Email Configuration CRUD
    "create_configuracion_correo", "get_configuracion_correo", "get_configuraciones_correo", "update_configuracion_correo", "delete_configuracion_correo",
    "create_historial_correo", "get_historial_correo", "get_historiales_correo", "update_historial_correo", "delete_historial_correo",
    
    # Payroll CRUD
    "create_periodo_nomina", "get_periodo_nomina", "get_periodos_nomina", "update_periodo_nomina", "delete_periodo_nomina",
    "create_nomina", "get_nomina", "get_nominas", "update_nomina", "delete_nomina",
    "create_percepcion", "get_percepcion", "get_percepciones", "update_percepcion", "delete_percepcion",
    "create_deduccion", "get_deduccion", "get_deducciones", "update_deduccion", "delete_deduccion",
    "create_incapacidad", "get_incapacidad", "get_incapacidades", "update_incapacidad", "delete_incapacidad",
    "create_otro_pago", "get_otro_pago", "get_otros_pagos", "update_otro_pago", "delete_otro_pago",
    
    # Agents CRUD
    "get_agent_tipo", "get_agent_tipo_by_name", "get_agent_tipos", "create_agent_tipo", "update_agent_tipo", "delete_agent_tipo",
    "get_agent_instalado", "get_active_agents_by_tipo", "get_agent_instalado_by_machine_and_tipo", "create_agent_instalado", 
    "update_agent_instalado", "register_agent_heartbeat", "delete_agent_instalado",
    "get_agent_tarea", "get_agent_tareas_by_agente", "get_agent_tareas_by_estado", "create_agent_tarea", 
    "update_agent_tarea", "assign_task_to_available_agent"
]