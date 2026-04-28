from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from decimal import Decimal
import logging
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.business_intelligence import Kpi, HistoricoKpi
from app.crud.business_intelligence import (
    get_active_kpis, create_historico_kpi, get_historico_kpi_by_kpi
)
from app.schemas.business_intelligence import HistoricoKpiCreate

logger = logging.getLogger(__name__)


class KPIService:
    """Servicio para el cálculo y gestión de KPIs"""
    
    @staticmethod
    def calculate_kpi_value(db: Session, kpi: Kpi) -> Decimal:
        """
        Calcula el valor actual de un KPI basado en su fórmula
        """
        # Este es un ejemplo básico. La implementación real dependerá de la complejidad de las fórmulas
        formula = kpi.formula.lower()
        
        try:
            # Aquí iría la lógica específica para cada tipo de KPI
            # Por ejemplo, para ventas: SELECT SUM(total) FROM sales WHERE date = TODAY
            if "ventas_totales" in formula:
                # Simulación de cálculo de ventas totales del día
                from app.models.sales import Venta
                today_sales = db.query(Venta).filter(
                    Venta.fecha_registro >= date.today(),
                    Venta.fecha_registro < date.today() + timedelta(days=1)
                ).with_entities(func.sum(Venta.total)).scalar() or 0
                
                return Decimal(str(today_sales))
                
            elif "clientes_nuevos" in formula:
                # Simulación de clientes nuevos del mes
                from app.models.hr import Cliente
                start_month = date.today().replace(day=1)
                end_month = start_month.replace(month=start_month.month+1) - timedelta(days=1)
                
                new_clients = db.query(Cliente).filter(
                    Cliente.fecha_registro >= start_month,
                    Cliente.fecha_registro <= end_month
                ).count()
                
                return Decimal(str(new_clients))
                
            else:
                # Para fórmulas más complejas, se podría usar un parser matemático
                # o una implementación específica por tipo de KPI
                logger.warning(f"Fórmula no reconocida para KPI {kpi.id}: {formula}")
                return Decimal("0")
                
        except Exception as e:
            logger.error(f"Error calculando KPI {kpi.id}: {str(e)}")
            return Decimal("0")
    
    @staticmethod
    def calculate_and_store_all_kpis(db: Session) -> Dict[str, Any]:
        """
        Calcula y almacena los valores de todos los KPIs activos
        """
        results = {
            "processed_count": 0,
            "success_count": 0,
            "errors": []
        }
        
        active_kpis = get_active_kpis(db)
        
        for kpi in active_kpis:
            try:
                # Calcular el valor del KPI
                calculated_value = KPIService.calculate_kpi_value(db, kpi)
                
                # Crear registro histórico
                historico_data = HistoricoKpiCreate(
                    kpi_id=kpi.id,
                    valor=calculated_value,
                    fecha_registro=date.today(),
                    fuente_datos="sistema"
                )
                
                create_historico_kpi(db, historico_data)
                results["success_count"] += 1
                
            except Exception as e:
                error_msg = f"Error procesando KPI {kpi.id}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
            
            results["processed_count"] += 1
        
        return results
    
    @staticmethod
    def get_kpi_trend(db: Session, kpi_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Obtiene la tendencia de un KPI para los últimos días especificados
        """
        from uuid import UUID
        from sqlalchemy import func
        
        start_date = date.today() - timedelta(days=days)
        end_date = date.today()
        
        historicos = get_historico_kpi_by_kpi(
            db=db,
            kpi_id=UUID(kpi_id),
            start_date=start_date,
            end_date=end_date
        )
        
        trend_data = []
        for record in historicos:
            trend_data.append({
                "date": record.fecha_registro.isoformat(),
                "value": float(record.valor),
                "formatted_value": str(record.valor)
            })
        
        return sorted(trend_data, key=lambda x: x["date"])
    
    @staticmethod
    def check_kpi_alerts(db: Session) -> List[Dict[str, Any]]:
        """
        Verifica si algún KPI activo supera su umbral de alerta
        """
        alerts = []
        active_kpis = get_active_kpis(db)
        
        for kpi in active_kpis:
            if kpi.umbral_alerta:
                # Obtener el valor más reciente
                latest_history = db.query(HistoricoKpi).filter(
                    HistoricoKpi.kpi_id == kpi.id
                ).order_by(HistoricoKpi.fecha_registro.desc()).first()
                
                if latest_history:
                    if latest_history.valor > kpi.umbral_alerta:
                        alerts.append({
                            "kpi_id": str(kpi.id),
                            "kpi_title": kpi.titulo,
                            "current_value": float(latest_history.valor),
                            "threshold": float(kpi.umbral_alerta),
                            "alert_type": "high"
                        })
                    elif kpi.meta_valor and latest_history.valor < kpi.meta_valor:
                        alerts.append({
                            "kpi_id": str(kpi.id),
                            "kpi_title": kpi.titulo,
                            "current_value": float(latest_history.valor),
                            "target": float(kpi.meta_valor or 0),
                            "alert_type": "low"
                        })
        
        return alerts