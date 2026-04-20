"""
SAT Mexico Chart of Accounts Import Service
Based on official SAT catalog for Mexican companies
"""

from sqlalchemy.orm import Session
from typing import List
import json
from pathlib import Path


def importar_catalogo_sat(db: Session) -> int:
    """Import SAT Mexico chart of accounts"""
    cuentas_sat = get_catalogo_sat_completo()
    
    count = 0
    for cuenta_data in cuentas_sat:
        existing = db.query(CuentaContable).filter(
            CuentaContable.codigo == cuenta_data['codigo']
        ).first()
        
        if not existing:
            from app.models.finance import CuentaContable
            db_cuenta = CuentaContable(**cuenta_data)
            db.add(db_cuenta)
            count += 1
    
    db.commit()
    return count


def get_catalogo_sat_completo() -> List[dict]:
    """
    Complete SAT chart of accounts for Mexico
    Based on Anexo 24 del Resolución Miscelánea Fiscal
    """
    return [
        # ============= ACTIVO (1) =============
        # Activo Circulante (11)
        {"codigo": "1101", "nombre": "Activo Circulante", "nivel": 2, "tipo": "activo", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "110101", "nombre": "Caja", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1101010001", "nombre": "Caja General", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101010002", "nombre": "Caja Chica", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        {"codigo": "110102", "nombre": "Bancos", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1101020001", "nombre": "Banco BBVA - Cuenta Cheques", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101020002", "nombre": "Banco Banorte - Cuenta Cheques", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101020003", "nombre": "Banco Santander - Cuenta Ahorro", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        {"codigo": "110103", "nombre": "Clientes", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1101030001", "nombre": "Clientes Nacionales", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101030002", "nombre": "Clientes Extranjeros", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101030003", "nombre": "Clientes - Sector Gobierno", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        {"codigo": "110104", "nombre": "Inventarios", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1101040001", "nombre": "Inventario Materia Prima", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040002", "nombre": "Inventario Producto en Proceso", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040003", "nombre": "Inventario Producto Terminado", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040004", "nombre": "Inventario Material de Empaque", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        {"codigo": "110105", "nombre": "IVA Acreditable", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1101050001", "nombre": "IVA Acreditable Compras Nacionales", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101050002", "nombre": "IVA Acreditable Importaciones", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101050003", "nombre": "IVA Acreditable Servicios", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        # Activo No Circulante (12)
        {"codigo": "1201", "nombre": "Activo No Circulante", "nivel": 2, "tipo": "activo", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "120101", "nombre": "Terrenos", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1201010001", "nombre": "Terrenos", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        {"codigo": "120102", "nombre": "Edificios", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1201020001", "nombre": "Edificios", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1201020002", "nombre": "Depreciación Acumulada Edificios", "nivel": 4, "tipo": "activo", "naturaleza": "acreedora"},
        
        {"codigo": "120103", "nombre": "Mobiliario y Equipo de Oficina", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1201030001", "nombre": "Mobiliario de Oficina", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1201030002", "nombre": "Equipo de Cómputo", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1201030003", "nombre": "Depreciación Acumulada Mob. y Equipo", "nivel": 4, "tipo": "activo", "naturaleza": "acreedora"},
        
        {"codigo": "120104", "nombre": "Maquinaria y Equipo Industrial", "nivel": 3, "tipo": "activo", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "1201040001", "nombre": "Máquinas de Coser", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1201040002", "nombre": "Máquinas de Corte", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1201040003", "nombre": "Depreciación Acumulada Maquinaria", "nivel": 4, "tipo": "activo", "naturaleza": "acreedora"},
        
        # ============= PASIVO (2) =============
        # Pasivo Circulante (21)
        {"codigo": "2101", "nombre": "Pasivo Circulante", "nivel": 2, "tipo": "pasivo", "naturaleza": "acreedora", "es_agrupadora": True},
        {"codigo": "210101", "nombre": "Proveedores Nacionales", "nivel": 3, "tipo": "pasivo", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "2101010001", "nombre": "Proveedores Materia Prima", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101010002", "nombre": "Proveedores Servicios", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        
        {"codigo": "210102", "nombre": "Cuentas por Pagar", "nivel": 3, "tipo": "pasivo", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "2101020001", "nombre": "Acreedores Diversos", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101020002", "nombre": "Documentos por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        
        {"codigo": "210103", "nombre": "Impuestos por Pagar", "nivel": 3, "tipo": "pasivo", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "2101030001", "nombre": "IVA Trasladado por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101030002", "nombre": "ISR por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101030003", "nombre": "IMSS por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101030004", "nombre": "INFONAVIT por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101030005", "nombre": "Retenciones ISR Sueldos", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2101030006", "nombre": "Retenciones IMSS Sueldos", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        
        {"codigo": "210104", "nombre": "Sueldos y Salarios por Pagar", "nivel": 3, "tipo": "pasivo", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "2101040001", "nombre": "Nómina por Pagar", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        
        # Pasivo No Circulante (22)
        {"codigo": "2201", "nombre": "Pasivo No Circulante", "nivel": 2, "tipo": "pasivo", "naturaleza": "acreedora", "es_agrupadora": True},
        {"codigo": "220101", "nombre": "Préstamos Bancarios Largo Plazo", "nivel": 3, "tipo": "pasivo", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "2201010001", "nombre": "Préstamos Bancarios L/P", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        {"codigo": "2201010002", "nombre": "Créditos Hipotecarios", "nivel": 4, "tipo": "pasivo", "naturaleza": "acreedora"},
        
        # ============= CAPITAL CONTABLE (3) =============
        {"codigo": "3101", "nombre": "Capital Contable", "nivel": 2, "tipo": "capital", "naturaleza": "acreedora", "es_agrupadora": True},
        {"codigo": "310101", "nombre": "Capital Social", "nivel": 3, "tipo": "capital", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "3101010001", "nombre": "Capital Social Fijo", "nivel": 4, "tipo": "capital", "naturaleza": "acreedora"},
        {"codigo": "3101010002", "nombre": "Aportaciones para Futuros Aumentos", "nivel": 4, "tipo": "capital", "naturaleza": "acreedora"},
        
        {"codigo": "310102", "nombre": "Utilidades Acumuladas", "nivel": 3, "tipo": "capital", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "3101020001", "nombre": "Utilidades Acumuladas Ejercicios Anteriores", "nivel": 4, "tipo": "capital", "naturaleza": "acreedora"},
        {"codigo": "3101020002", "nombre": "Pérdidas Acumuladas", "nivel": 4, "tipo": "capital", "naturaleza": "deudora"},
        
        {"codigo": "310103", "nombre": "Resultado del Ejercicio", "nivel": 3, "tipo": "capital", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "3101030001", "nombre": "Utilidad del Ejercicio", "nivel": 4, "tipo": "capital", "naturaleza": "acreedora"},
        {"codigo": "3101030002", "nombre": "Pérdida del Ejercicio", "nivel": 4, "tipo": "capital", "naturaleza": "deudora"},
        
        # ============= INGRESOS (4) =============
        {"codigo": "4101", "nombre": "Ingresos por Ventas", "nivel": 2, "tipo": "ingresos", "naturaleza": "acreedora", "es_agrupadora": True},
        {"codigo": "410101", "nombre": "Ventas de Producto Terminado", "nivel": 3, "tipo": "ingresos", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "4101010001", "nombre": "Ventas Guayaberas", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        {"codigo": "4101010002", "nombre": "Ventas Camisas", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        {"codigo": "4101010003", "nombre": "Ventas Otras Prendas", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        
        {"codigo": "410102", "nombre": "Ventas de Servicio", "nivel": 3, "tipo": "ingresos", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "4101020001", "nombre": "Servicios de Confección por Terceros", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        {"codigo": "4101020002", "nombre": "Servicios de Bordado", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        
        {"codigo": "4102", "nombre": "Devoluciones y Descuentos", "nivel": 2, "tipo": "ingresos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "410201", "nombre": "Devoluciones sobre Ventas", "nivel": 3, "tipo": "ingresos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "4102010001", "nombre": "Devoluciones Guayaberas", "nivel": 4, "tipo": "ingresos", "naturaleza": "deudora"},
        
        {"codigo": "4103", "nombre": "Otros Ingresos", "nivel": 2, "tipo": "ingresos", "naturaleza": "acreedora", "es_agrupadora": True},
        {"codigo": "410301", "nombre": "Ingresos Financieros", "nivel": 3, "tipo": "ingresos", "naturaleza": "acreedora", "es_cuenta_mayor": True},
        {"codigo": "4103010001", "nombre": "Intereses Bancarios", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        {"codigo": "4103010002", "nombre": "Rendimientos Financieros", "nivel": 4, "tipo": "ingresos", "naturaleza": "acreedora"},
        
        # ============= COSTOS (5) =============
        {"codigo": "5101", "nombre": "Costo de Ventas", "nivel": 2, "tipo": "costos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "510101", "nombre": "Costo de Producción", "nivel": 3, "tipo": "costos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "5101010001", "nombre": "Materia Prima Consumida", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5101010002", "nombre": "Mano de Obra Directa", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5101010003", "nombre": "Gastos Indirectos de Producción", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        
        {"codigo": "5102", "nombre": "Compras", "nivel": 2, "tipo": "costos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "510201", "nombre": "Compras de Materia Prima", "nivel": 3, "tipo": "costos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "5102010001", "nombre": "Compras de Telas", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5102010002", "nombre": "Compras de Hilos", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5102010003", "nombre": "Compras de Botones", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5102010004", "nombre": "Compras de Insumos", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        
        # ============= GASTOS (6) =============
        # Gastos de Operación (61)
        {"codigo": "6101", "nombre": "Gastos de Operación", "nivel": 2, "tipo": "gastos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "610101", "nombre": "Gastos de Venta", "nivel": 3, "tipo": "gastos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "6101010001", "nombre": "Sueldos Vendedores", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101010002", "nombre": "Comisiones sobre Ventas", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101010003", "nombre": "Publicidad y Propaganda", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        
        {"codigo": "610102", "nombre": "Gastos de Administración", "nivel": 3, "tipo": "gastos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "6101020001", "nombre": "Sueldos Administrativos", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101020002", "nombre": "Renta de Oficina", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101020003", "nombre": "Servicios Públicos (Agua, Luz, Teléfono)", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101020004", "nombre": "Papelería y Útiles de Oficina", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101020005", "nombre": "Software y Suscripciones", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101020006", "nombre": "Honorarios Contables", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        
        {"codigo": "610103", "nombre": "Gastos de Producción", "nivel": 3, "tipo": "gastos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "6101030001", "nombre": "Renta de Taller", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101030002", "nombre": "Mantenimiento de Máquinas", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6101030003", "nombre": "Herramental y Refacciones", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        
        # Gastos Financieros (62)
        {"codigo": "6201", "nombre": "Gastos Financieros", "nivel": 2, "tipo": "gastos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "620101", "nombre": "Intereses Bancarios", "nivel": 3, "tipo": "gastos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "6201010001", "nombre": "Comisiones Bancarias", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        {"codigo": "6201010002", "nombre": "Intereses por Préstamos", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
        
        {"codigo": "6202", "nombre": "Pérdida Cambiaria", "nivel": 2, "tipo": "gastos", "naturaleza": "deudora", "es_agrupadora": True},
        {"codigo": "620201", "nombre": "Pérdida en Tipo de Cambio", "nivel": 3, "tipo": "gastos", "naturaleza": "deudora", "es_cuenta_mayor": True},
        {"codigo": "6202010001", "nombre": "Pérdida Cambiaria", "nivel": 4, "tipo": "gastos", "naturaleza": "deudora"},
    ]


def get_cuentas_textiles() -> List[dict]:
    """
    Special accounts for textile/garment industry
    These are additions to the SAT catalog specific to guayabera production
    """
    return [
        # Inventario específico textil
        {"codigo": "1101040005", "nombre": "Inventario Telas por Rollo", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040006", "nombre": "Inventario Telas por Retazo", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040007", "nombre": "Inventario Hilos y Bordados", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040008", "nombre": "Inventario Accesorios (Botones, Cierre, etc.)", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        # Producción en proceso textil
        {"codigo": "1101040009", "nombre": "WIP - Corte", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040010", "nombre": "WIP - Costura", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040011", "nombre": "WIP - Planchado y Acabado", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        # Producto terminado por tipo
        {"codigo": "1101040012", "nombre": "PT - Guayaberas Blancas", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040013", "nombre": "PT - Guayaberas Color", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040014", "nombre": "PT - Camisas", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        {"codigo": "1101040015", "nombre": "PT - Otras Prendas", "nivel": 4, "tipo": "activo", "naturaleza": "deudora"},
        
        # Costos de producción textil
        {"codigo": "5101010004", "nombre": "Consumo de Tela", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5101010005", "nombre": "Consumo de Hilo", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5101010006", "nombre": "Consumo de Botones", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
        {"codigo": "5101010007", "nombre": "Merma de Producción", "nivel": 4, "tipo": "costos", "naturaleza": "deudora"},
    ]
