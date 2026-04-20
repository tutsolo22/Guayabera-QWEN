"""
Examples of automatic accounting entries for different modules

This file shows how other modules (compras, ventas, nomina, produccion)
should integrate with the automatic accounting system.
"""

# ============================================================
# EJEMPLO 1: MÓDULO DE COMPRAS
# ============================================================

"""
When a purchase order is created, automatic accounting entries are generated.

Database impact:
- Inventario MP increases
- Proveedores increases

Accounting entry:
Débito:  Inventario Materia Prima (1101040001)
Crédito: Proveedores Nacionales (2101010001)
         IVA Acreditable (1101050001)
"""

async def crear_orden_compra_example():
    """Example function for purchase order creation"""
    
    # Your purchase order logic here
    orden_compra = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "proveedor": "Telas Yucatán SA",
        "fecha": "2025-11-23",
        "total": 11600.00,
        "concepto": "50m de tela blanca"
    }
    
    # Define accounting movements
    movimientos_contables = [
        {
            "cuenta_codigo": "1101040001",  # Inventario MP
            "cargo": 10000.00,
            "abono": 0,
            "concepto": f"Compra de tela - {orden_compra['proveedor']}",
            "documento_referencia": f"OC-{orden_compra['id'][:8]}"
        },
        {
            "cuenta_codigo": "1101050001",  # IVA Acreditable
            "cargo": 1600.00,
            "abono": 0,
            "concepto": "IVA 16% compra de tela",
            "documento_referencia": f"OC-{orden_compra['id'][:8]}"
        },
        {
            "cuenta_codigo": "2101010001",  # Proveedores Nacionales
            "cargo": 0,
            "abono": 11600.00,
            "concepto": f"Compra a crédito - {orden_compra['proveedor']}",
            "documento_referencia": f"OC-{orden_compra['id'][:8]}"
        }
    ]
    
    # Create automatic accounting entry
    from app.services.automatic_accounting import AutomaticAccountingService
    
    # This would be called after saving the purchase order
    # service.create_automatic_entry(
    #     modulo_origen="compras",
    #     entidad_origen="orden_compra",
    #     entidad_id=orden_compra["id"],
    #     movimientos=movimientos_contables,
    #     fecha=orden_compra["fecha"],
    #     descripcion=f"Compra de {orden_compra['concepto']}",
    #     referencia=f"OC-{orden_compra['id'][:8]}",
    #     datos_origen=orden_compra
    # )
    
    return {
        **orden_compra,
        "movimientos_contables": movimientos_contables,
        "mensaje": "Orden de compra creada y asiento contable generado"
    }


# ============================================================
# EJEMPLO 2: MÓDULO DE VENTAS
# ============================================================

"""
When a sale is made, automatic accounting entries are generated.

Database impact:
- Cuentas por cobrar increases
- Ventas increases
- IVA por pagar increases

Accounting entry:
Débito:  Clientes Nacionales (1101030001)
Crédito: Ventas Guayaberas (4101010001)
         IVA Trasladado (2101030001)
"""

async def crear_factura_venta_example():
    """Example function for sales invoice creation"""
    
    # Your sales logic here
    factura = {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "cliente": "Boutique Elegante",
        "fecha": "2025-11-23",
        "total": 23200.00,
        "subtotal": 20000.00,
        "iva": 3200.00,
        "concepto": "20 guayaberas blancas talla M"
    }
    
    # Define accounting movements
    movimientos_contables = [
        {
            "cuenta_codigo": "1101030001",  # Clientes Nacionales
            "cargo": 23200.00,
            "abono": 0,
            "concepto": f"Venta a crédito - {factura['cliente']}",
            "documento_referencia": f"FAC-{factura['id'][:8]}"
        },
        {
            "cuenta_codigo": "4101010001",  # Ventas Guayaberas
            "cargo": 0,
            "abono": 20000.00,
            "concepto": f"Venta de {factura['concepto']}",
            "documento_referencia": f"FAC-{factura['id'][:8]}"
        },
        {
            "cuenta_codigo": "2101030001",  # IVA Trasladado
            "cargo": 0,
            "abono": 3200.00,
            "concepto": "IVA 16% venta de guayaberas",
            "documento_referencia": f"FAC-{factura['id'][:8]}"
        }
    ]
    
    return {
        **factura,
        "movimientos_contables": movimientos_contables,
        "mensaje": "Factura creada y asiento contable generado"
    }


# ============================================================
# EJEMPLO 3: MÓDULO DE PRODUCCIÓN
# ============================================================

"""
When production is completed, automatic accounting entries are generated.

Database impact:
- Inventario PT increases
- WIP decreases
- Materia prima consumida

Accounting entry:
Débito:  Inventario PT (1101040012)
Crédito: WIP - Costura (1101040010)
         Mano de Obra Directa (5101010002)
"""

async def finalizar_orden_produccion_example():
    """Example function for production order completion"""
    
    # Your production logic here
    orden_produccion = {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "producto": "Guayabera Blanca Talla M",
        "cantidad": 100,
        "fecha": "2025-11-23",
        "costo_unitario": 150.00,
        "costo_total": 15000.00,
        "desglose": {
            "materia_prima": 8000.00,
            "mano_obra": 5000.00,
            "gastos_indirectos": 2000.00
        }
    }
    
    # Define accounting movements
    movimientos_contables = [
        {
            "cuenta_codigo": "1101040012",  # PT - Guayaberas Blancas
            "cargo": 15000.00,
            "abono": 0,
            "concepto": f"Producción terminada - {orden_produccion['cantidad']} {orden_produccion['producto']}",
            "documento_referencia": f"OP-{orden_produccion['id'][:8]}"
        },
        {
            "cuenta_codigo": "1101040010",  # WIP - Costura
            "cargo": 0,
            "abono": 10000.00,
            "concepto": "Transferencia de WIP a PT",
            "documento_referencia": f"OP-{orden_produccion['id'][:8]}"
        },
        {
            "cuenta_codigo": "5101010002",  # Mano de Obra Directa
            "cargo": 0,
            "abono": 5000.00,
            "concepto": "Mano de obra consumida en producción",
            "documento_referencia": f"OP-{orden_produccion['id'][:8]}"
        }
    ]
    
    return {
        **orden_produccion,
        "movimientos_contables": movimientos_contables,
        "mensaje": "Producción finalizada y asiento contable generado"
    }


# ============================================================
# EJEMPLO 4: MÓDULO DE NÓMINA
# ============================================================

"""
When payroll is processed, automatic accounting entries are generated.

Database impact:
- Gastos de nómina increases
- Impuestos por pagar increases
- Sueldos por pagar increases

Accounting entry:
Débito:  Sueldos Administrativos (6101020001)
         IMSS Patronal (610103000X)
Crédito: Sueldos por Pagar (2101040001)
         IMSS por Pagar (2101030003)
         ISR por Pagar (2101030002)
"""

async def procesar_nomina_example():
    """Example function for payroll processing"""
    
    # Your payroll logic here
    nomina = {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "periodo": "2025-11-16 a 2025-11-30",
        "fecha_pago": "2025-11-30",
        "total_sueldos": 50000.00,
        "total_imss_patronal": 8000.00,
        "retenciones_isr": 5000.00,
        "retenciones_imss": 2000.00,
        "neto_pagar": 43000.00,
        "empleados": 10
    }
    
    # Define accounting movements
    movimientos_contables = [
        {
            "cuenta_codigo": "6101020001",  # Sueldos Administrativos
            "cargo": 50000.00,
            "abono": 0,
            "concepto": f"Nómina quincenal - {nomina['empleados']} empleados",
            "documento_referencia": f"NOM-{nomina['id'][:8]}"
        },
        {
            "cuenta_codigo": "6101030001",  # IMSS Patronal
            "cargo": 8000.00,
            "abono": 0,
            "concepto": "IMSS patronal",
            "documento_referencia": f"NOM-{nomina['id'][:8]}"
        },
        {
            "cuenta_codigo": "2101040001",  # Sueldos por Pagar
            "cargo": 0,
            "abono": 43000.00,
            "concepto": "Sueldos netos por pagar",
            "documento_referencia": f"NOM-{nomina['id'][:8]}"
        },
        {
            "cuenta_codigo": "2101030002",  # ISR por Pagar
            "cargo": 0,
            "abono": 5000.00,
            "concepto": "Retención ISR empleados",
            "documento_referencia": f"NOM-{nomina['id'][:8]}"
        },
        {
            "cuenta_codigo": "2101030003",  # IMSS por Pagar
            "cargo": 0,
            "abono": 10000.00,
            "concepto": "IMSS (patrón + empleados)",
            "documento_referencia": f"NOM-{nomina['id'][:8]}"
        }
    ]
    
    return {
        **nomina,
        "movimientos_contables": movimientos_contables,
        "mensaje": "Nómina procesada y asiento contable generado"
    }


# ============================================================
# EJEMPLO 5: MÓDULO DE PAGOS DE BANCOS
# ============================================================

"""
When a bank payment is made, automatic accounting entries are generated.

Database impact:
- Proveedores decreases
- Bancos decreases

Accounting entry:
Débito:  Proveedores Nacionales (2101010001)
Crédito: Banco BBVA (1101020001)
"""

async def realizar_pago_bancario_example():
    """Example function for bank payment"""
    
    # Your payment logic here
    pago = {
        "id": "990e8400-e29b-41d4-a716-446655440004",
        "banco": "BBVA",
        "cuenta": "1234567890",
        "fecha": "2025-11-23",
        "monto": 11600.00,
        "beneficiario": "Telas Yucatán SA",
        "concepto": "Pago factura OC-2025-001"
    }
    
    # Define accounting movements
    movimientos_contables = [
        {
            "cuenta_codigo": "2101010001",  # Proveedores Nacionales
            "cargo": 11600.00,
            "abono": 0,
            "concepto": f"Pago a {pago['beneficiario']}",
            "documento_referencia": f"PAGO-{pago['id'][:8]}"
        },
        {
            "cuenta_codigo": "1101020001",  # Banco BBVA
            "cargo": 0,
            "abono": 11600.00,
            "concepto": f"Pago por {pago['concepto']}",
            "documento_referencia": f"PAGO-{pago['id'][:8]}"
        }
    ]
    
    return {
        **pago,
        "movimientos_contables": movimientos_contables,
        "mensaje": "Pago realizado y asiento contable generado"
    }


# ============================================================
# RESUMEN DE INTEGRACIÓN
# ============================================================

"""
Para integrar cualquier módulo con el sistema de asientos automáticos:

1. DEFINIR MOVIMIENTOS CONTABLES:
   - Cada movimiento debe tener: cuenta_codigo, cargo o abono, concepto
   - La suma de cargos debe ser igual a la suma de abonos
   - Usar cuentas del catálogo SAT importado

2. LLAMAR AL SERVICIO DESPUÉS DE GUARDAR:
   ```python
   from app.services.automatic_accounting import AutomaticAccountingService
   
   service = AutomaticAccountingService(db)
   service.create_automatic_entry(
       modulo_origen="nombre_modulo",
       entidad_origen="tipo_entidad",
       entidad_id=entity_id,
       movimientos=movimientos_contables,
       fecha=entity.fecha,
       descripcion=f"Descripción del asiento",
       referencia=f"REF-{entity.id[:8]}",
       datos_origen=entity.dict()
   )
   ```

3. USAR CELERY PARA NO BLOQUEAR:
   ```python
   from app.workers.tasks import create_automatic_entry_async
   
   create_automatic_entry_async.delay(
       modulo_origen="nombre_modulo",
       entidad_origen="tipo_entidad",
       entidad_id=str(entity_id),
       movimientos=movimientos_contables,
       ...
   )
   ```

4. MONITOREAR ERRORES:
   - GET /api/v1/finance/automaticos/monitoreo
   - GET /api/v1/finance/automaticos/estadisticas
   - Revisar logs de Celery worker
"""
