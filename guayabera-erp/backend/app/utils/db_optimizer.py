"""
Database Optimizer: Utilities for optimizing database queries and indexing
Implements query optimization techniques and helps with index management
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def optimize_query_performance(session: Session, query_sql: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze and optimize a SQL query
    :param session: SQLAlchemy session
    :param query_sql: Raw SQL query to analyze
    :param params: Parameters for the query
    :return: Analysis and optimization suggestions
    """
    analysis = {
        "original_query": query_sql,
        "execution_plan": "",
        "suggestions": [],
        "estimated_cost": 0
    }
    
    try:
        # Get execution plan
        plan_query = f"EXPLAIN ANALYZE {query_sql}"
        result = session.execute(text(plan_query), params or {})
        
        plan_lines = []
        for row in result:
            plan_lines.append(str(row))
        
        analysis["execution_plan"] = "\n".join(plan_lines)
        
        # Look for potential optimizations
        plan_text = analysis["execution_plan"].lower()
        
        if "seq scan" in plan_text:
            analysis["suggestions"].append("Consider adding indexes to avoid sequential scans")
        
        if "nested loop" in plan_text and "inner join" in query_sql.lower():
            analysis["suggestions"].append("Consider rewriting JOINs to use hash or merge joins instead of nested loops")
        
        if "sort" in plan_text:
            analysis["suggestions"].append("Consider adding ORDER BY indexes or rewriting query to avoid sorting")
        
        # Estimate cost based on plan
        if "cost=" in plan_text:
            import re
            costs = re.findall(r"cost=(\d+\.\d+)", plan_text)
            if costs:
                analysis["estimated_cost"] = float(costs[0])
    
    except Exception as e:
        logger.error(f"Error analyzing query: {str(e)}")
        analysis["error"] = str(e)
    
    return analysis


def suggest_indexes(session: Session, table_name: str) -> List[Dict[str, str]]:
    """
    Suggest indexes for a table based on query patterns
    :param session: SQLAlchemy session
    :param table_name: Name of the table
    :return: List of suggested indexes
    """
    suggestions = []
    
    try:
        # Get table columns
        columns_query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        """
        result = session.execute(text(columns_query))
        
        columns = []
        for row in result:
            columns.append({
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == 'YES'
            })
        
        # Suggest indexes based on column types and usage patterns
        for col in columns:
            if "id" in col["name"] and col["name"] != "id":
                suggestions.append({
                    "column": col["name"],
                    "type": "BTREE",
                    "reason": "Foreign key columns benefit from indexing"
                })
            
            if "fecha" in col["name"] or "date" in col["name"].lower():
                suggestions.append({
                    "column": col["name"],
                    "type": "BTREE",
                    "reason": "Date columns commonly used in WHERE clauses"
                })
            
            if "rfc" in col["name"].lower() or "clave" in col["name"].lower():
                suggestions.append({
                    "column": col["name"],
                    "type": "BTREE",
                    "reason": "Unique identifier columns benefit from indexing"
                })
        
        # Suggest composite indexes for common query patterns
        if any("fecha" in col["name"] or "date" in col["name"].lower() for col in columns):
            # Look for potential composite indexes
            date_cols = [col["name"] for col in columns if "fecha" in col["name"] or "date" in col["name"].lower()]
            id_cols = [col["name"] for col in columns if "id" in col["name"]]
            
            if date_cols and id_cols:
                suggestions.append({
                    "column": f"{date_cols[0]}, {id_cols[0]}",
                    "type": "COMPOSITE BTREE",
                    "reason": "Common pattern: filtering by date and ID"
                })
    
    except Exception as e:
        logger.error(f"Error suggesting indexes for {table_name}: {str(e)}")
    
    return suggestions


def create_index(session: Session, table_name: str, column_name: str, index_type: str = "BTREE") -> bool:
    """
    Create an index on a table column
    :param session: SQLAlchemy session
    :param table_name: Name of the table
    :param column_name: Name of the column(s) to index
    :param index_type: Type of index to create
    :return: True if successful, False otherwise
    """
    try:
        # Handle composite indexes
        if "," in column_name:
            # Create a name for the composite index
            clean_columns = "_".join(col.strip().replace("_", "") for col in column_name.split(","))
            index_name = f"idx_{table_name}_{clean_columns}"
            columns_part = column_name
        else:
            index_name = f"idx_{table_name}_{column_name.replace('_', '')}"
            columns_part = column_name
        
        create_query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} USING {index_type} ({columns_part})"
        session.execute(text(create_query))
        session.commit()
        
        logger.info(f"Created index {index_name} on {table_name}({column_name})")
        return True
    except Exception as e:
        logger.error(f"Error creating index on {table_name}({column_name}): {str(e)}")
        session.rollback()
        return False


def get_slow_queries(session: Session, threshold_ms: int = 100) -> List[Dict[str, Any]]:
    """
    Get slow queries from the database logs (PostgreSQL specific)
    :param session: SQLAlchemy session
    :param threshold_ms: Threshold in milliseconds for slow queries
    :return: List of slow queries
    """
    slow_queries = []
    
    try:
        # Query PostgreSQL's pg_stat_statements extension if available
        check_extension = "SELECT installed_version FROM pg_available_extensions WHERE name = 'pg_stat_statements'"
        result = session.execute(text(check_extension))
        extension_row = result.fetchone()
        
        if extension_row and extension_row[0] is not None:
            # Extension is available, get slow queries
            slow_query = f"""
            SELECT 
                query, 
                mean_time, 
                calls, 
                total_time, 
                rows
            FROM pg_stat_statements 
            WHERE mean_time > {threshold_ms}
            ORDER BY mean_time DESC
            LIMIT 10
            """
            result = session.execute(text(slow_query))
            
            for row in result:
                slow_queries.append({
                    "query": row[0],
                    "mean_time_ms": round(float(row[1]), 2),
                    "calls": row[2],
                    "total_time_ms": round(float(row[3]), 2),
                    "rows": row[4]
                })
        else:
            # Alternative: Log our own slow queries
            logger.warning("pg_stat_statements extension not available, consider enabling it for better query insights")
    
    except Exception as e:
        logger.error(f"Error getting slow queries: {str(e)}")
    
    return slow_queries


def analyze_table_stats(session: Session, table_name: str) -> Dict[str, Any]:
    """
    Analyze statistics for a table
    :param session: SQLAlchemy session
    :param table_name: Name of the table
    :return: Statistics about the table
    """
    stats = {
        "table_name": table_name,
        "row_count": 0,
        "size_mb": 0,
        "last_analyzed": None,
        "columns": [],
        "recommendations": []
    }
    
    try:
        # Get row count
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        result = session.execute(text(count_query))
        stats["row_count"] = result.scalar()
        
        # Get table size
        size_query = f"SELECT pg_size_pretty(pg_total_relation_size('{table_name}'))"
        result = session.execute(text(size_query))
        size_str = result.scalar()
        # Convert to MB
        if "kB" in size_str:
            stats["size_mb"] = float(size_str.replace("kB", "").strip()) / 1024
        elif "MB" in size_str:
            stats["size_mb"] = float(size_str.replace("MB", "").strip())
        elif "GB" in size_str:
            stats["size_mb"] = float(size_str.replace("GB", "").strip()) * 1024
        else:
            stats["size_mb"] = 0.01  # Small table
        
        # Get column information
        col_query = f"""
        SELECT 
            column_name, 
            data_type, 
            is_nullable, 
            column_default
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
        """
        result = session.execute(text(col_query))
        
        for row in result:
            stats["columns"].append({
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == 'YES',
                "default": row[3]
            })
        
        # Make recommendations based on stats
        if stats["row_count"] > 100000:  # Large table
            stats["recommendations"].append("Consider partitioning this large table")
            stats["recommendations"].append("Ensure all foreign keys have indexes")
        
        if stats["size_mb"] > 100:  # Large table (>100MB)
            stats["recommendations"].append("Monitor this large table for performance issues")
        
        nullable_text_fields = [
            col["name"] for col in stats["columns"] 
            if col["type"] in ['text', 'varchar'] and col["nullable"]
        ]
        if nullable_text_fields:
            stats["recommendations"].append(f"Consider indexing these nullable text fields: {', '.join(nullable_text_fields)}")
    
    except Exception as e:
        logger.error(f"Error analyzing table {table_name}: {str(e)}")
        stats["error"] = str(e)
    
    return stats