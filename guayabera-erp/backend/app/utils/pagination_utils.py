"""
Pagination Utilities: Optimized pagination for large datasets
Implements efficient pagination strategies for large result sets
"""

from typing import TypeVar, Generic, List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from math import ceil
import json

T = TypeVar('T')


class PageParams(BaseModel):
    """
    Parameters for pagination
    """
    page: int = 1
    page_size: int = 20
    sort_field: Optional[str] = None
    sort_direction: str = "asc"  # asc or desc


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Response model for paginated results
    """
    items: List[T]
    total_items: int
    current_page: int
    total_pages: int
    page_size: int
    has_previous: bool
    has_next: bool
    next_cursor: Optional[str] = None  # For cursor-based pagination
    prev_cursor: Optional[str] = None  # For cursor-based pagination


def paginate_query(
    db: Session,
    query,
    params: PageParams,
    transform_func=None
) -> PaginatedResponse:
    """
    Efficiently paginate a SQLAlchemy query
    :param db: Database session
    :param query: SQLAlchemy query object
    :param params: Pagination parameters
    :param transform_func: Optional function to transform results
    :return: Paginated response
    """
    # Calculate offset
    offset = (params.page - 1) * params.page_size
    
    # Apply sorting if specified
    if params.sort_field:
        if params.sort_direction.lower() == "desc":
            query = query.order_by(getattr(query.column_descriptions[0]['entities'][0], params.sort_field).desc())
        else:
            query = query.order_by(getattr(query.column_descriptions[0]['entities'][0], params.sort_field).asc())
    
    # Get total count (we'll optimize this later)
    total_items = query.count()
    
    # Apply pagination
    items = query.offset(offset).limit(params.page_size).all()
    
    # Transform items if needed
    if transform_func:
        items = [transform_func(item) for item in items]
    
    # Calculate pagination metadata
    total_pages = ceil(total_items / params.page_size)
    
    response = PaginatedResponse(
        items=items,
        total_items=total_items,
        current_page=params.page,
        total_pages=total_pages,
        page_size=params.page_size,
        has_previous=params.page > 1,
        has_next=params.page < total_pages
    )
    
    return response


def optimized_paginate_query(
    db: Session,
    base_query,
    count_query,
    params: PageParams,
    transform_func=None
) -> PaginatedResponse:
    """
    More optimized pagination that separates count query from data query
    :param db: Database session
    :param base_query: SQLAlchemy query for fetching data
    :param count_query: Separate query for counting (can be optimized)
    :param params: Pagination parameters
    :param transform_func: Optional function to transform results
    :return: Paginated response
    """
    # Calculate offset
    offset = (params.page - 1) * params.page_size
    
    # Apply sorting if specified
    if params.sort_field:
        if params.sort_direction.lower() == "desc":
            base_query = base_query.order_by(getattr(base_query.column_descriptions[0]['entities'][0], params.sort_field).desc())
        else:
            base_query = base_query.order_by(getattr(base_query.column_descriptions[0]['entities'][0], params.sort_field).asc())
    
    # Execute count query separately (potentially optimized)
    total_items = db.execute(count_query).scalar()
    
    # Apply pagination to base query
    items = base_query.offset(offset).limit(params.page_size).all()
    
    # Transform items if needed
    if transform_func:
        items = [transform_func(item) for item in items]
    
    # Calculate pagination metadata
    total_pages = ceil(total_items / params.page_size)
    
    response = PaginatedResponse(
        items=items,
        total_items=total_items,
        current_page=params.page,
        total_pages=total_pages,
        page_size=params.page_size,
        has_previous=params.page > 1,
        has_next=params.page < total_pages
    )
    
    return response


def cursor_paginate_query(
    db: Session,
    base_query,
    cursor_field: str,
    cursor_value: Optional[str] = None,
    page_size: int = 20,
    sort_direction: str = "asc",
    transform_func=None
) -> PaginatedResponse:
    """
    Cursor-based pagination for better performance on large datasets
    :param db: Database session
    :param base_query: SQLAlchemy query for fetching data
    :param cursor_field: Field to use as cursor (should be indexed)
    :param cursor_value: Current cursor value (None for first page)
    :param page_size: Number of items per page
    :param sort_direction: Direction to sort ('asc' or 'desc')
    :param transform_func: Optional function to transform results
    :return: Paginated response with cursors
    """
    # Apply sorting
    entity = base_query.column_descriptions[0]['entities'][0]
    field_attr = getattr(entity, cursor_field)
    
    if sort_direction.lower() == "desc":
        base_query = base_query.order_by(field_attr.desc())
        condition_op = "<" if sort_direction.lower() == "asc" else ">"
    else:
        base_query = base_query.order_by(field_attr.asc())
        condition_op = ">" if sort_direction.lower() == "asc" else "<"
    
    # Apply cursor filter if provided
    if cursor_value is not None:
        try:
            # Try to convert cursor value to appropriate type
            if cursor_value.isdigit():
                cursor_value = int(cursor_value)
            elif cursor_value.replace('.', '').isdigit():
                cursor_value = float(cursor_value)
        except ValueError:
            pass  # Keep as string
        
        base_query = base_query.filter(field_attr.op(condition_op)(cursor_value))
    
    # Fetch one extra to determine if there's a next page
    items = base_query.limit(page_size + 1).all()
    
    # Check if there are more items
    has_next = len(items) > page_size
    if has_next:
        items = items[:-1]  # Remove the extra item
    
    # Transform items if needed
    if transform_func:
        items = [transform_func(item) for item in items]
    
    # Calculate next/prev cursors
    next_cursor = None
    prev_cursor = cursor_value  # Previous cursor is the current one
    
    if items and has_next:
        last_item = items[-1]
        next_cursor = str(getattr(last_item, cursor_field))
    
    # For previous cursor, we would need another query in real implementation
    # This is simplified for now
    
    response = PaginatedResponse(
        items=items,
        total_items=len(items),  # We don't have the total count with cursor pagination
        current_page=1,  # Cursor pagination doesn't use traditional page numbers
        total_pages=0,  # Not applicable with cursor pagination
        page_size=page_size,
        has_previous=cursor_value is not None,
        has_next=has_next,
        next_cursor=next_cursor,
        prev_cursor=prev_cursor
    )
    
    return response


def get_optimized_count(db: Session, table_name: str, conditions: Optional[str] = None) -> int:
    """
    Get count using an optimized approach
    :param db: Database session
    :param table_name: Name of the table to count
    :param conditions: Optional WHERE conditions
    :return: Count of records
    """
    where_clause = f"WHERE {conditions}" if conditions else ""
    
    # Try approximate count first for large tables
    approx_query = f"""
    SELECT reltuples::BIGINT AS estimate
    FROM pg_class
    WHERE relname = '{table_name}';
    """
    
    try:
        result = db.execute(text(approx_query))
        estimate = result.scalar()
        
        # If estimate is significantly large, use a sampling approach
        if estimate and estimate > 100000:
            # For very large tables, we can use TABLESAMPLE to get a quick estimate
            sample_query = f"SELECT COUNT(*) * 100 FROM {table_name} TABLESAMPLE SYSTEM (1);"
            result = db.execute(text(sample_query))
            sampled_count = result.scalar()
            
            # If sampled count is still significant, return the estimate
            if sampled_count > 1000:
                return estimate
        
        # Otherwise, do an exact count
        count_query = f"SELECT COUNT(*) FROM {table_name} {where_clause};"
        result = db.execute(text(count_query))
        return result.scalar()
    
    except Exception as e:
        # Fallback to exact count if anything goes wrong
        count_query = f"SELECT COUNT(*) FROM {table_name} {where_clause};"
        result = db.execute(text(count_query))
        return result.scalar()


def create_pagination_metadata(current_page: int, total_pages: int, total_items: int, page_size: int) -> dict:
    """
    Create pagination metadata
    :param current_page: Current page number
    :param total_pages: Total number of pages
    :param total_items: Total number of items
    :param page_size: Size of each page
    :return: Dictionary with pagination metadata
    """
    return {
        "current_page": current_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "page_size": page_size,
        "has_previous": current_page > 1,
        "has_next": current_page < total_pages,
        "previous_page": current_page - 1 if current_page > 1 else None,
        "next_page": current_page + 1 if current_page < total_pages else None,
        "range_start": (current_page - 1) * page_size + 1,
        "range_end": min(current_page * page_size, total_items)
    }