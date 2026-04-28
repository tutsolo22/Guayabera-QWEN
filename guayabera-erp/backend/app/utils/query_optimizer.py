"""
Query Optimizer: Strategies for optimizing database queries
Implements various optimization techniques to improve query performance
"""

from sqlalchemy.orm import Session, joinedload, selectinload, contains_eager
from sqlalchemy import and_, or_, text
from typing import Type, List, Any, Optional, Callable
import time
import logging

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """
    Class to implement various query optimization strategies
    """
    
    @staticmethod
    def optimize_joins(session: Session, base_query, relationships: List[str]):
        """
        Optimize queries with joins using appropriate loading strategies
        :param session: SQLAlchemy session
        :param base_query: Base query to optimize
        :param relationships: List of relationship names to load
        :return: Optimized query
        """
        optimized_query = base_query
        
        for relationship in relationships:
            # Use selectinload for many-to-one or one-to-one lazy loads
            # Use joinedload for cases where we need to filter on related data
            optimized_query = optimized_query.options(selectinload(relationship))
        
        return optimized_query
    
    @staticmethod
    def eager_load_relationships(session: Session, base_query, relationships: List[str], strategy: str = "selectin"):
        """
        Eager load relationships using specified strategy
        :param session: SQLAlchemy session
        :param base_query: Base query to optimize
        :param relationships: List of relationship names to load
        :param strategy: Loading strategy ("selectin", "joined", or "subquery")
        :return: Query with eager-loaded relationships
        """
        optimized_query = base_query
        
        for relationship in relationships:
            if strategy == "selectin":
                optimized_query = optimized_query.options(selectinload(relationship))
            elif strategy == "joined":
                optimized_query = optimized_query.options(joinedload(relationship))
            elif strategy == "contains_eager":
                optimized_query = optimized_query.options(contains_eager(relationship))
            else:
                logger.warning(f"Unknown loading strategy: {strategy}, using selectinload")
                optimized_query = optimized_query.options(selectinload(relationship))
        
        return optimized_query
    
    @staticmethod
    def apply_filters_dynamically(base_query, filters: dict):
        """
        Apply filters dynamically to a query
        :param base_query: Base query to apply filters to
        :param filters: Dictionary of filters to apply
        :return: Query with applied filters
        """
        query = base_query
        
        for field, value in filters.items():
            if value is not None and value != "":
                # Handle different filter types
                if isinstance(value, dict):
                    # Range filters: {"min": 10, "max": 20}
                    if "min" in value:
                        query = query.filter(getattr(type(base_query._entities[0].entity), field) >= value["min"])
                    if "max" in value:
                        query = query.filter(getattr(type(base_query._entities[0].entity), field) <= value["max"])
                    if "in" in value:
                        query = query.filter(getattr(type(base_query._entities[0].entity), field).in_(value["in"]))
                elif isinstance(value, list):
                    # In filters: [1, 2, 3]
                    query = query.filter(getattr(type(base_query._entities[0].entity), field).in_(value))
                else:
                    # Simple equality filter
                    query = query.filter(getattr(type(base_query._entities[0].entity), field) == value)
        
        return query
    
    @staticmethod
    def optimize_for_list_view(session: Session, model: Type[Any], filters: dict = None, 
                              relationships: List[str] = None, limit: int = None):
        """
        Optimize query for list views with common patterns
        :param session: SQLAlchemy session
        :param model: Model class to query
        :param filters: Filters to apply
        :param relationships: Relationships to eager-load
        :param limit: Limit on results
        :return: Optimized query results
        """
        query = session.query(model)
        
        # Apply filters if provided
        if filters:
            query = QueryOptimizer.apply_filters_dynamically(query, filters)
        
        # Apply relationship optimizations
        if relationships:
            query = QueryOptimizer.eager_load_relationships(session, query, relationships, "selectin")
        
        # Apply limit if provided
        if limit:
            query = query.limit(limit)
        
        start_time = time.time()
        results = query.all()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow query detected in optimize_for_list_view: {elapsed_time:.2f}s for {model.__name__}")
        
        return results
    
    @staticmethod
    def optimize_for_search(session: Session, model: Type[Any], search_term: str, 
                           search_fields: List[str], filters: dict = None):
        """
        Optimize query for search functionality
        :param session: SQLAlchemy session
        :param model: Model class to query
        :param search_term: Term to search for
        :param search_fields: Fields to search in
        :param filters: Additional filters to apply
        :return: Search results
        """
        query = session.query(model)
        
        # Build search conditions
        search_conditions = []
        for field in search_fields:
            search_conditions.append(getattr(model, field).ilike(f"%{search_term}%"))
        
        if search_conditions:
            query = query.filter(or_(*search_conditions))
        
        # Apply additional filters
        if filters:
            query = QueryOptimizer.apply_filters_dynamically(query, filters)
        
        start_time = time.time()
        results = query.all()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow search query detected: {elapsed_time:.2f}s for {model.__name__}")
        
        return results
    
    @staticmethod
    def optimize_aggregate_query(session: Session, model: Type[Any], 
                                aggregate_functions: List[tuple], 
                                group_by: List[str] = None,
                                filters: dict = None):
        """
        Optimize aggregate queries (COUNT, SUM, AVG, etc.)
        :param session: SQLAlchemy session
        :param model: Model class to query
        :param aggregate_functions: List of tuples (function, field) to apply
        :param group_by: Fields to group by
        :param filters: Filters to apply
        :return: Aggregate results
        """
        from sqlalchemy import func
        
        # Build aggregation query
        agg_fields = []
        for agg_func, field in aggregate_functions:
            if agg_func == "count":
                agg_fields.append(func.count(getattr(model, field)).label(f"count_{field}"))
            elif agg_func == "sum":
                agg_fields.append(func.sum(getattr(model, field)).label(f"sum_{field}"))
            elif agg_func == "avg":
                agg_fields.append(func.avg(getattr(model, field)).label(f"avg_{field}"))
            elif agg_func == "max":
                agg_fields.append(func.max(getattr(model, field)).label(f"max_{field}"))
            elif agg_func == "min":
                agg_fields.append(func.min(getattr(model, field)).label(f"min_{field}"))
        
        query = session.query(*agg_fields)
        
        # Apply filters
        if filters:
            query = QueryOptimizer.apply_filters_dynamically(query, filters)
        
        # Apply group by if specified
        if group_by:
            group_fields = [getattr(model, field) for field in group_by]
            query = query.group_by(*group_fields)
        
        start_time = time.time()
        results = query.all()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow aggregate query detected: {elapsed_time:.2f}s for {model.__name__}")
        
        return results
    
    @staticmethod
    def optimize_complex_query(session: Session, base_query, 
                             joins: List[tuple] = None,
                             filters: dict = None,
                             relationships: List[str] = None,
                             order_by: str = None,
                             order_direction: str = "ASC",
                             limit: int = None,
                             offset: int = None):
        """
        Optimize complex queries with multiple operations
        :param session: SQLAlchemy session
        :param base_query: Base query to optimize
        :param joins: List of (model, condition) tuples to join
        :param filters: Filters to apply
        :param relationships: Relationships to eager-load
        :param order_by: Field to order by
        :param order_direction: Direction to order ("ASC" or "DESC")
        :param limit: Limit on results
        :param offset: Offset for results
        :return: Optimized query results
        """
        query = base_query
        
        # Apply joins
        if joins:
            for join_model, join_condition in joins:
                query = query.join(join_model, join_condition)
        
        # Apply filters
        if filters:
            query = QueryOptimizer.apply_filters_dynamically(query, filters)
        
        # Apply relationship optimizations
        if relationships:
            query = QueryOptimizer.eager_load_relationships(session, query, relationships, "selectin")
        
        # Apply ordering
        if order_by:
            model_attr = getattr(type(base_query._entities[0].entity), order_by)
            if order_direction.upper() == "DESC":
                query = query.order_by(model_attr.desc())
            else:
                query = query.order_by(model_attr.asc())
        
        # Apply limit and offset
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        
        start_time = time.time()
        results = query.all()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow complex query detected: {elapsed_time:.2f}s")
        
        return results


def create_optimized_query_builder(session: Session, model: Type[Any]):
    """
    Factory function to create an optimized query builder for a specific model
    :param session: SQLAlchemy session
    :param model: Model class to create builder for
    :return: OptimizedQueryBuilder instance
    """
    return OptimizedQueryBuilder(session, model)


class OptimizedQueryBuilder:
    """
    Builder pattern for constructing optimized queries
    """
    
    def __init__(self, session: Session, model: Type[Any]):
        self.session = session
        self.model = model
        self.query = session.query(model)
        self._applied_joins = set()
        self._eager_loaded = []
    
    def join_model(self, join_model: Type[Any], condition: Any):
        """
        Join with another model
        :param join_model: Model to join with
        :param condition: Join condition
        :return: Self for chaining
        """
        if join_model not in self._applied_joins:
            self.query = self.query.join(join_model, condition)
            self._applied_joins.add(join_model)
        return self
    
    def filter_by(self, **filters):
        """
        Apply filters to the query
        :param filters: Filter conditions
        :return: Self for chaining
        """
        self.query = self.query.filter_by(**filters)
        return self
    
    def filter(self, *filter_conditions):
        """
        Apply filter conditions to the query
        :param filter_conditions: Filter conditions
        :return: Self for chaining
        """
        self.query = self.query.filter(*filter_conditions)
        return self
    
    def eager_load(self, relationship: str, strategy: str = "selectin"):
        """
        Eager load a relationship
        :param relationship: Relationship to load
        :param strategy: Loading strategy
        :return: Self for chaining
        """
        if strategy == "selectin":
            self.query = self.query.options(selectinload(relationship))
        elif strategy == "joined":
            self.query = self.query.options(joinedload(relationship))
        elif strategy == "contains_eager":
            self.query = self.query.options(contains_eager(relationship))
        
        self._eager_loaded.append(relationship)
        return self
    
    def order_by_field(self, field_name: str, direction: str = "ASC"):
        """
        Order the query by a field
        :param field_name: Name of field to order by
        :param direction: Direction to order ("ASC" or "DESC")
        :return: Self for chaining
        """
        field = getattr(self.model, field_name)
        if direction.upper() == "DESC":
            self.query = self.query.order_by(field.desc())
        else:
            self.query = self.query.order_by(field.asc())
        return self
    
    def limit_results(self, limit: int):
        """
        Limit the number of results
        :param limit: Maximum number of results
        :return: Self for chaining
        """
        self.query = self.query.limit(limit)
        return self
    
    def offset_results(self, offset: int):
        """
        Set the offset for results
        :param offset: Number of results to skip
        :return: Self for chaining
        """
        self.query = self.query.offset(offset)
        return self
    
    def execute(self):
        """
        Execute the query and return results
        :return: Query results
        """
        start_time = time.time()
        results = self.query.all()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow query builder execution: {elapsed_time:.2f}s for {self.model.__name__}")
        
        return results
    
    def count(self):
        """
        Count the number of results without loading them
        :return: Count of results
        """
        return self.query.count()