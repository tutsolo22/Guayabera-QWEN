"""
Health Checks and Monitoring: System monitoring and health check endpoints
Provides comprehensive monitoring capabilities for the ERP system
"""

import asyncio
import time
import psutil
import socket
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine


@dataclass
class HealthStatus:
    """Data class to hold health check results"""
    status: str
    details: Dict[str, Any]
    timestamp: datetime
    response_time: float


class SystemMonitor:
    """
    Comprehensive system monitoring class
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def check_system_health(self) -> HealthStatus:
        """
        Perform a comprehensive system health check
        :return: HealthStatus object with system status
        """
        start_time = time.time()
        
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Check memory usage
        memory = psutil.virtual_memory()
        
        # Check disk usage
        disk_usage = psutil.disk_usage('/')
        
        # Check network connectivity
        network_io = psutil.net_io_counters()
        
        # Collect system metrics
        system_metrics = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_percent": disk_usage.percent,
            "disk_free_gb": round(disk_usage.free / (1024**3), 2),
            "network_bytes_sent": network_io.bytes_sent,
            "network_bytes_recv": network_io.bytes_recv,
            "uptime_seconds": time.time() - psutil.boot_time(),
        }
        
        # Determine overall status based on thresholds
        status = "healthy"
        if cpu_percent > 90 or memory.percent > 90 or disk_usage.percent > 95:
            status = "degraded"
        
        response_time = time.time() - start_time
        
        return HealthStatus(
            status=status,
            details={"system_metrics": system_metrics},
            timestamp=datetime.utcnow(),
            response_time=response_time
        )
    
    def check_database_health(self, db: Session) -> HealthStatus:
        """
        Check database connectivity and performance
        :param db: Database session
        :return: HealthStatus object with database status
        """
        start_time = time.time()
        
        try:
            # Test basic connectivity
            result = db.execute(text("SELECT 1")).fetchone()
            
            # Test performance with a simple query
            perf_start = time.time()
            db.execute(text("SELECT COUNT(*) FROM information_schema.tables")).fetchone()
            perf_time = time.time() - perf_start
            
            # Check connection pool status
            conn_info = {
                "connected": True,
                "query_response_time": perf_time,
                "connection_test": result[0] if result else None
            }
            
            status = "healthy" if perf_time < 0.5 else "degraded"
            
            response_time = time.time() - start_time
            
            return HealthStatus(
                status=status,
                details={"database": conn_info},
                timestamp=datetime.utcnow(),
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthStatus(
                status="unhealthy",
                details={"database": {"connected": False, "error": str(e)}},
                timestamp=datetime.utcnow(),
                response_time=response_time
            )
    
    def check_cache_health(self) -> HealthStatus:
        """
        Check cache (Redis) connectivity and performance
        :return: HealthStatus object with cache status
        """
        start_time = time.time()
        
        try:
            import redis
            from app.core.config import settings
            
            # Connect to Redis
            redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                password=settings.REDIS_PASSWORD,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test basic ping
            ping_result = redis_client.ping()
            
            # Test performance with a simple set/get operation
            perf_start = time.time()
            test_key = f"health_check_{int(time.time())}"
            redis_client.setex(test_key, 10, "test_value")
            retrieved_value = redis_client.get(test_key)
            perf_time = time.time() - perf_start
            
            cache_info = {
                "connected": ping_result,
                "ping_response_time": perf_time,
                "test_operation_success": retrieved_value == b"test_value"
            }
            
            status = "healthy" if ping_result and perf_time < 0.1 else "degraded"
            
            response_time = time.time() - start_time
            
            return HealthStatus(
                status=status,
                details={"cache": cache_info},
                timestamp=datetime.utcnow(),
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthStatus(
                status="unhealthy",
                details={"cache": {"connected": False, "error": str(e)}},
                timestamp=datetime.utcnow(),
                response_time=response_time
            )
    
    def check_external_services(self) -> HealthStatus:
        """
        Check connectivity to external services (Facturama, etc.)
        :return: HealthStatus object with external services status
        """
        start_time = time.time()
        
        external_services = {}
        status = "healthy"
        
        # Check Facturama connectivity by attempting to connect to their API endpoint
        try:
            import requests
            facturama_start = time.time()
            
            # Just check if we can reach the base URL (without making a real API call)
            response = requests.head("https://apisandbox.facturama.mx/", timeout=10)
            facturama_time = time.time() - facturama_start
            
            external_services["facturama"] = {
                "reachable": response.status_code < 500,
                "response_time": facturama_time,
                "status_code": response.status_code
            }
            
            if response.status_code >= 400:
                status = "degraded"
                
        except Exception as e:
            external_services["facturama"] = {
                "reachable": False,
                "error": str(e)
            }
            status = "degraded"
        
        # Check SMTP connectivity
        try:
            smtp_start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)  # 10 second timeout
            result = sock.connect_ex((settings.SMTP_SERVER, settings.SMTP_PORT))
            sock.close()
            smtp_time = time.time() - smtp_start
            
            external_services["smtp"] = {
                "reachable": result == 0,
                "response_time": smtp_time
            }
            
            if result != 0:
                status = "degraded"
                
        except Exception as e:
            external_services["smtp"] = {
                "reachable": False,
                "error": str(e)
            }
            status = "degraded"
        
        response_time = time.time() - start_time
        
        return HealthStatus(
            status=status,
            details={"external_services": external_services},
            timestamp=datetime.utcnow(),
            response_time=response_time
        )
    
    def get_detailed_health_report(self, db: Session) -> Dict[str, Any]:
        """
        Get a comprehensive health report for the entire system
        :param db: Database session
        :return: Detailed health report
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "system": self.check_system_health(),
            "database": self.check_database_health(db),
            "cache": self.check_cache_health(),
            "external_services": self.check_external_services(),
        }
        
        # Calculate overall status based on individual checks
        statuses = [
            report["system"].status,
            report["database"].status,
            report["cache"].status,
            report["external_services"].status
        ]
        
        if "unhealthy" in statuses:
            overall_status = "unhealthy"
        elif "degraded" in statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"
        
        report["overall_status"] = overall_status
        
        # Convert HealthStatus objects to dictionaries for JSON serialization
        for key in ["system", "database", "cache", "external_services"]:
            health_obj = report[key]
            report[key] = {
                "status": health_obj.status,
                "details": health_obj.details,
                "timestamp": health_obj.timestamp.isoformat(),
                "response_time": health_obj.response_time
            }
        
        return report
    
    def get_performance_metrics(self, db: Session) -> Dict[str, Any]:
        """
        Get detailed performance metrics
        :param db: Database session
        :return: Performance metrics
        """
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        
        # Database metrics
        db_metrics = {}
        try:
            # Get active connections
            active_conn_query = """
            SELECT COUNT(*) FROM pg_stat_activity 
            WHERE datname = current_database() 
            AND state = 'active';
            """
            active_connections = db.execute(text(active_conn_query)).scalar()
            
            # Get slow queries (queries taking more than 1 second)
            slow_query = """
            SELECT query, mean_time 
            FROM pg_stat_statements 
            WHERE mean_time > 1000
            ORDER BY mean_time DESC
            LIMIT 5;
            """
            
            try:
                slow_results = db.execute(text(slow_query)).fetchall()
                slow_queries = [{"query": row[0][:100] + "..." if len(row[0]) > 100 else row[0], 
                                "mean_time_ms": round(row[1], 2)} for row in slow_results]
            except:
                slow_queries = []  # pg_stat_statements might not be enabled
            
            db_metrics = {
                "active_connections": active_connections,
                "slow_queries": slow_queries
            }
        except Exception as e:
            db_metrics = {"error": str(e)}
        
        # Cache metrics
        try:
            import redis
            from app.core.config import settings
            
            redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                password=settings.REDIS_PASSWORD
            )
            
            info = redis_client.info()
            cache_metrics = {
                "used_memory": info.get('used_memory_human', 'unknown'),
                "connected_clients": info.get('connected_clients', 0),
                "total_commands_processed": info.get('total_commands_processed', 0),
                "keyspace_hits": info.get('keyspace_hits', 0),
                "keyspace_misses": info.get('keyspace_misses', 0),
                "hit_rate": (info.get('keyspace_hits', 0) / 
                            max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1), 1)) * 100
            }
        except Exception as e:
            cache_metrics = {"error": str(e)}
        
        return {
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk_usage.percent,
                "disk_free_gb": round(disk_usage.free / (1024**3), 2),
            },
            "database": db_metrics,
            "cache": cache_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }


# Create a global monitor instance
monitor = SystemMonitor()