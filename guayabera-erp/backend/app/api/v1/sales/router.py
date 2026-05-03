from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.sales import (
    SalesConfigurationCreate,
    SalesConfigurationUpdate,
    SalesConfigurationResponse,
    DiscountRuleCreate,
    DiscountRuleUpdate,
    DiscountRuleResponse,
    LoyaltyProgramCreate,
    LoyaltyProgramUpdate,
    LoyaltyProgramResponse,
    PriceListCreate,
    PriceListUpdate,
    PriceListResponse,
    PriceListItemCreate,
    PriceListItemUpdate,
    PriceListItemResponse,
    PriceListWithItemsResponse
)
from app.crud.sales import (
    create_sales_configuration,
    get_sales_configuration,
    update_sales_configuration,
    delete_sales_configuration,
    create_discount_rule,
    get_discount_rule,
    get_discount_rules_by_company,
    update_discount_rule,
    delete_discount_rule,
    get_active_discount_rules,
    create_loyalty_program,
    get_loyalty_program,
    get_loyalty_programs_by_company,
    get_default_loyalty_program,
    update_loyalty_program,
    delete_loyalty_program,
    create_price_list,
    get_price_list,
    get_price_lists_by_company,
    get_default_price_list,
    update_price_list,
    delete_price_list,
    create_price_list_item,
    get_price_list_item,
    get_price_list_items_by_list,
    get_price_list_item_by_product_and_list,
    update_price_list_item,
    delete_price_list_item,
    get_current_price_for_product
)
from app.crud.security import create_audit_log
from app.models.security import AuditLog

router = APIRouter(prefix="/sales-config", tags=["sales-config"])


# Función auxiliar para registrar eventos de auditoría
def log_audit_event(
    db: Session,
    request: Request,
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[int] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    notes: Optional[str] = None
):
    try:
        audit_data = {
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "old_values": old_values,
            "new_values": new_values,
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "notes": notes
        }
        create_audit_log(db, audit_data)
    except Exception:
        # Si falla la auditoría, no debe afectar la operación principal
        pass


# Rutas para SalesConfiguration
@router.post("/configuration/", response_model=SalesConfigurationResponse)
def create_sales_config(
    request: Request,
    config: SalesConfigurationCreate, 
    db: Session = Depends(get_db)
):
    """Crear una configuración de ventas para una empresa"""
    # Verificar si ya existe una configuración para esta empresa
    existing_config = get_sales_configuration(db, config.company_id)
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una configuración para esta empresa"
        )
    
    result = create_sales_configuration(db=db, config=config)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, config.created_by, "create", "sales_configuration", 
        result.id, None, config.dict(), "Creación de configuración de ventas"
    )
    
    return result


@router.get("/configuration/{company_id}", response_model=SalesConfigurationResponse)
def get_sales_config(company_id: int, db: Session = Depends(get_db)):
    """Obtener la configuración de ventas para una empresa"""
    config = get_sales_configuration(db, company_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de ventas no encontrada"
        )
    
    return config


@router.put("/configuration/{company_id}", response_model=SalesConfigurationResponse)
def update_sales_config(
    request: Request,
    company_id: int, 
    config_update: SalesConfigurationUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar la configuración de ventas para una empresa"""
    # Obtener configuración actual antes de actualizar
    old_config = get_sales_configuration(db, company_id)
    if not old_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de ventas no encontrada"
        )
    
    old_values = {
        "price_update_approval_required": old_config.price_update_approval_required,
        "allow_manual_discounts": old_config.allow_manual_discounts,
        "max_discount_percentage": float(old_config.max_discount_percentage),
        "enable_promotions": old_config.enable_promotions,
        "promotion_approval_required": old_config.promotion_approval_required,
        "enable_customer_loyalty": old_config.enable_customer_loyalty,
        "loyalty_points_per_currency": float(old_config.loyalty_points_per_currency),
        "points_to_currency_ratio": float(old_config.points_to_currency_ratio),
        "require_sales_order_approval": old_config.require_sales_order_approval,
        "allow_backorders": old_config.allow_backorders,
        "default_sales_terms": old_config.default_sales_terms,
        "default_tax_rate": float(old_config.default_tax_rate),
    }
    
    config = update_sales_configuration(db=db, company_id=company_id, config_update=config_update)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, config.created_by, "update", "sales_configuration", 
        config.id, old_values, config_update.dict(exclude_unset=True), 
        "Actualización de configuración de ventas"
    )
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de ventas no encontrada"
        )
    return config


@router.delete("/configuration/{company_id}")
def delete_sales_config(
    request: Request,
    company_id: int, 
    db: Session = Depends(get_db)
):
    """Eliminar la configuración de ventas para una empresa"""
    config = get_sales_configuration(db, company_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de ventas no encontrada"
        )
    
    old_values = {
        "price_update_approval_required": config.price_update_approval_required,
        "allow_manual_discounts": config.allow_manual_discounts,
        "max_discount_percentage": float(config.max_discount_percentage),
        "enable_promotions": config.enable_promotions,
        "promotion_approval_required": config.promotion_approval_required,
        "enable_customer_loyalty": config.enable_customer_loyalty,
        "loyalty_points_per_currency": float(config.loyalty_points_per_currency),
        "points_to_currency_ratio": float(config.points_to_currency_ratio),
        "require_sales_order_approval": config.require_sales_order_approval,
        "allow_backorders": config.allow_backorders,
        "default_sales_terms": config.default_sales_terms,
        "default_tax_rate": float(config.default_tax_rate),
    }
    
    result = delete_sales_configuration(db=db, company_id=company_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de ventas no encontrada"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, config.created_by, "delete", "sales_configuration", 
        config.id, old_values, None, 
        "Eliminación de configuración de ventas"
    )
    
    return {"message": "Configuración de ventas eliminada exitosamente"}


# Rutas para DiscountRule
@router.post("/discount-rules/", response_model=DiscountRuleResponse)
def create_discount_r(
    request: Request,
    route: DiscountRuleCreate, 
    db: Session = Depends(get_db)
):
    """Crear una regla de descuento"""
    result = create_discount_rule(db=db, rule=route)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, route.created_by, "create", "discount_rule", 
        result.id, None, route.dict(), "Creación de regla de descuento"
    )
    
    return result


@router.get("/discount-rules/{rule_id}", response_model=DiscountRuleResponse)
def get_discount_r(rule_id: int, db: Session = Depends(get_db)):
    """Obtener una regla de descuento por ID"""
    rule = get_discount_rule(db, rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla de descuento no encontrada"
        )
    return rule


@router.get("/discount-rules/company/{company_id}", response_model=List[DiscountRuleResponse])
def get_discount_rules(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener reglas de descuento por empresa"""
    return get_discount_rules_by_company(db, company_id, skip=skip, limit=limit)


@router.get("/discount-rules/company/{company_id}/active", response_model=List[DiscountRuleResponse])
def get_active_discount_rules_by_company(company_id: int, db: Session = Depends(get_db)):
    """Obtener reglas de descuento activas por empresa"""
    return get_active_discount_rules(db, company_id)


@router.put("/discount-rules/{rule_id}", response_model=DiscountRuleResponse)
def update_discount_r(
    request: Request,
    rule_id: int,
    rule_update: DiscountRuleUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una regla de descuento"""
    # Obtener regla actual antes de actualizar
    old_rule = get_discount_rule(db, rule_id)
    if not old_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla de descuento no encontrada"
        )
    
    old_values = {
        "name": old_rule.name,
        "description": old_rule.description,
        "discount_type": old_rule.discount_type,
        "discount_value": float(old_rule.discount_value),
        "min_quantity": old_rule.min_quantity,
        "min_amount": float(old_rule.min_amount),
        "applies_to_all_products": old_rule.applies_to_all_products,
        "start_date": old_rule.start_date.isoformat() if old_rule.start_date else None,
        "end_date": old_rule.end_date.isoformat() if old_rule.end_date else None,
        "is_active": old_rule.is_active,
        "priority": old_rule.priority,
    }
    
    rule = update_discount_rule(db=db, rule_id=rule_id, rule_update=rule_update)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla de descuento no encontrada"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, rule.created_by, "update", "discount_rule", 
        rule.id, old_values, rule_update.dict(exclude_unset=True), 
        "Actualización de regla de descuento"
    )
    
    return rule


@router.delete("/discount-rules/{rule_id}")
def delete_discount_r(
    request: Request,
    rule_id: int, 
    db: Session = Depends(get_db)
):
    """Eliminar una regla de descuento"""
    rule = get_discount_rule(db, rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla de descuento no encontrada"
        )
    
    old_values = {
        "name": rule.name,
        "description": rule.description,
        "discount_type": rule.discount_type,
        "discount_value": float(rule.discount_value),
        "min_quantity": rule.min_quantity,
        "min_amount": float(rule.min_amount),
        "applies_to_all_products": rule.applies_to_all_products,
        "start_date": rule.start_date.isoformat() if rule.start_date else None,
        "end_date": rule.end_date.isoformat() if rule.end_date else None,
        "is_active": rule.is_active,
        "priority": rule.priority,
    }
    
    result = delete_discount_rule(db=db, rule_id=rule_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla de descuento no encontrada"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, rule.created_by, "delete", "discount_rule", 
        rule.id, old_values, None, 
        "Eliminación de regla de descuento"
    )
    
    return {"message": "Regla de descuento eliminada exitosamente"}


# Rutas para LoyaltyProgram
@router.post("/loyalty-programs/", response_model=LoyaltyProgramResponse)
def create_loyalty_pgm(
    request: Request,
    program: LoyaltyProgramCreate, 
    db: Session = Depends(get_db)
):
    """Crear un programa de lealtad"""
    result = create_loyalty_program(db=db, program=program)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, program.created_by, "create", "loyalty_program", 
        result.id, None, program.dict(), "Creación de programa de lealtad"
    )
    
    return result


@router.get("/loyalty-programs/{program_id}", response_model=LoyaltyProgramResponse)
def get_loyalty_pgm(program_id: int, db: Session = Depends(get_db)):
    """Obtener un programa de lealtad por ID"""
    program = get_loyalty_program(db, program_id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de lealtad no encontrado"
        )
    return program


@router.get("/loyalty-programs/company/{company_id}", response_model=List[LoyaltyProgramResponse])
def get_loyalty_programs(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener programas de lealtad por empresa"""
    return get_loyalty_programs_by_company(db, company_id, skip=skip, limit=limit)


@router.get("/loyalty-programs/company/{company_id}/default", response_model=Optional[LoyaltyProgramResponse])
def get_default_loyalty_pgm(company_id: int, db: Session = Depends(get_db)):
    """Obtener el programa de lealtad predeterminado de una empresa"""
    program = get_default_loyalty_program(db, company_id)
    return program


@router.put("/loyalty-programs/{program_id}", response_model=LoyaltyProgramResponse)
def update_loyalty_pgm(
    request: Request,
    program_id: int,
    program_update: LoyaltyProgramUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un programa de lealtad"""
    # Obtener programa actual antes de actualizar
    old_program = get_loyalty_program(db, program_id)
    if not old_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de lealtad no encontrado"
        )
    
    old_values = {
        "name": old_program.name,
        "description": old_program.description,
        "earning_method": old_program.earning_method,
        "points_calculation": old_program.points_calculation,
        "earning_rate": float(old_program.earning_rate),
        "redemption_rate": float(old_program.redemption_rate),
        "minimum_points_for_redemption": old_program.minimum_points_for_redemption,
        "points_expire": old_program.points_expire,
        "points_expiry_months": old_program.points_expiry_months,
        "is_active": old_program.is_active,
        "is_default": old_program.is_default,
    }
    
    program = update_loyalty_program(db=db, program_id=program_id, program_update=program_update)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de lealtad no encontrado"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, program.created_by, "update", "loyalty_program", 
        program.id, old_values, program_update.dict(exclude_unset=True), 
        "Actualización de programa de lealtad"
    )
    
    return program


@router.delete("/loyalty-programs/{program_id}")
def delete_loyalty_pgm(
    request: Request,
    program_id: int, 
    db: Session = Depends(get_db)
):
    """Eliminar un programa de lealtad"""
    program = get_loyalty_program(db, program_id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de lealtad no encontrado"
        )
    
    old_values = {
        "name": program.name,
        "description": program.description,
        "earning_method": program.earning_method,
        "points_calculation": program.points_calculation,
        "earning_rate": float(program.earning_rate),
        "redemption_rate": float(program.redemption_rate),
        "minimum_points_for_redemption": program.minimum_points_for_redemption,
        "points_expire": program.points_expire,
        "points_expiry_months": program.points_expiry_months,
        "is_active": program.is_active,
        "is_default": program.is_default,
    }
    
    result = delete_loyalty_program(db=db, program_id=program_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de lealtad no encontrado"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, program.created_by, "delete", "loyalty_program", 
        program.id, old_values, None, 
        "Eliminación de programa de lealtad"
    )
    
    return {"message": "Programa de lealtad eliminado exitosamente"}


# Rutas para PriceList
@router.post("/price-lists/", response_model=PriceListResponse)
def create_price_l(
    request: Request,
    price_list: PriceListCreate, 
    db: Session = Depends(get_db)
):
    """Crear una lista de precios"""
    result = create_price_list(db=db, price_list=price_list)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, price_list.created_by, "create", "price_list", 
        result.id, None, price_list.dict(), "Creación de lista de precios"
    )
    
    return result


@router.get("/price-lists/{price_list_id}", response_model=PriceListWithItemsResponse)
def get_price_l(price_list_id: int, db: Session = Depends(get_db)):
    """Obtener una lista de precios con sus items"""
    price_list = get_price_list(db, price_list_id)
    if not price_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de precios no encontrada"
        )
    
    # Agregar los items a la respuesta
    items = get_price_list_items_by_list(db, price_list_id, skip=0, limit=1000)
    price_list.items = items
    return price_list


@router.get("/price-lists/company/{company_id}", response_model=List[PriceListResponse])
def get_price_lists(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener listas de precios por empresa"""
    return get_price_lists_by_company(db, company_id, skip=skip, limit=limit)


@router.get("/price-lists/company/{company_id}/default", response_model=Optional[PriceListResponse])
def get_default_price_l(company_id: int, db: Session = Depends(get_db)):
    """Obtener la lista de precios predeterminada de una empresa"""
    price_list = get_default_price_list(db, company_id)
    return price_list


@router.put("/price-lists/{price_list_id}", response_model=PriceListResponse)
def update_price_l(
    request: Request,
    price_list_id: int,
    price_list_update: PriceListUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una lista de precios"""
    # Obtener lista actual antes de actualizar
    old_list = get_price_list(db, price_list_id)
    if not old_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de precios no encontrada"
        )
    
    old_values = {
        "name": old_list.name,
        "description": old_list.description,
        "currency": old_list.currency,
        "is_active": old_list.is_active,
        "is_default": old_list.is_default,
        "valid_from": old_list.valid_from.isoformat() if old_list.valid_from else None,
        "valid_until": old_list.valid_until.isoformat() if old_list.valid_until else None,
    }
    
    price_list = update_price_list(db=db, price_list_id=price_list_id, price_list_update=price_list_update)
    if not price_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de precios no encontrada"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, price_list.created_by, "update", "price_list", 
        price_list.id, old_values, price_list_update.dict(exclude_unset=True), 
        "Actualización de lista de precios"
    )
    
    return price_list


@router.delete("/price-lists/{price_list_id}")
def delete_price_l(
    request: Request,
    price_list_id: int, 
    db: Session = Depends(get_db)
):
    """Eliminar una lista de precios"""
    price_list = get_price_list(db, price_list_id)
    if not price_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de precios no encontrada"
        )
    
    old_values = {
        "name": price_list.name,
        "description": price_list.description,
        "currency": price_list.currency,
        "is_active": price_list.is_active,
        "is_default": price_list.is_default,
        "valid_from": price_list.valid_from.isoformat() if price_list.valid_from else None,
        "valid_until": price_list.valid_until.isoformat() if price_list.valid_until else None,
    }
    
    result = delete_price_list(db=db, price_list_id=price_list_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de precios no encontrada"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, price_list.created_by, "delete", "price_list", 
        price_list.id, old_values, None, 
        "Eliminación de lista de precios"
    )
    
    return {"message": "Lista de precios eliminada exitosamente"}


# Rutas para PriceListItem
@router.post("/price-list-items/", response_model=PriceListItemResponse)
def create_price_list_it(
    request: Request,
    item: PriceListItemCreate, 
    db: Session = Depends(get_db)
):
    """Crear un ítem en una lista de precios"""
    result = create_price_list_item(db=db, item=item)
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, None, "create", "price_list_item", 
        result.id, None, item.dict(), "Creación de ítem de lista de precios"
    )
    
    return result


@router.get("/price-list-items/{item_id}", response_model=PriceListItemResponse)
def get_price_list_it(item_id: int, db: Session = Depends(get_db)):
    """Obtener un ítem de lista de precios por ID"""
    item = get_price_list_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ítem de lista de precios no encontrado"
        )
    return item


@router.get("/price-list-items/list/{price_list_id}", response_model=List[PriceListItemResponse])
def get_price_list_items(
    price_list_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener ítems de una lista de precios"""
    return get_price_list_items_by_list(db, price_list_id, skip=skip, limit=limit)


@router.put("/price-list-items/{item_id}", response_model=PriceListItemResponse)
def update_price_list_it(
    request: Request,
    item_id: int,
    item_update: PriceListItemUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un ítem en una lista de precios"""
    # Obtener ítem actual antes de actualizar
    old_item = get_price_list_item(db, item_id)
    if not old_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ítem de lista de precios no encontrado"
        )
    
    old_values = {
        "price": float(old_item.price),
        "currency": old_item.currency,
        "valid_from": old_item.valid_from.isoformat() if old_item.valid_from else None,
        "valid_until": old_item.valid_until.isoformat() if old_item.valid_until else None,
    }
    
    item = update_price_list_item(db=db, item_id=item_id, item_update=item_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ítem de lista de precios no encontrado"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, None, "update", "price_list_item", 
        item.id, old_values, item_update.dict(exclude_unset=True), 
        "Actualización de ítem de lista de precios"
    )
    
    return item


@router.delete("/price-list-items/{item_id}")
def delete_price_list_it(
    request: Request,
    item_id: int, 
    db: Session = Depends(get_db)
):
    """Eliminar un ítem de una lista de precios"""
    item = get_price_list_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ítem de lista de precios no encontrado"
        )
    
    old_values = {
        "price": float(item.price),
        "currency": item.currency,
        "valid_from": item.valid_from.isoformat() if item.valid_from else None,
        "valid_until": item.valid_until.isoformat() if item.valid_until else None,
    }
    
    result = delete_price_list_item(db=db, item_id=item_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ítem de lista de precios no encontrado"
        )
    
    # Registrar evento de auditoría
    log_audit_event(
        db, request, None, "delete", "price_list_item", 
        item.id, old_values, None, 
        "Eliminación de ítem de lista de precios"
    )
    
    return {"message": "Ítem de lista de precios eliminado exitosamente"}


@router.get("/price-list-items/current-price/{price_list_id}/{product_variant_id}")
def get_current_price(
    price_list_id: int,
    product_variant_id: int,
    db: Session = Depends(get_db)
):
    """Obtener el precio actual para un producto en una lista de precios específica"""
    price = get_current_price_for_product(db, price_list_id, product_variant_id)
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Precio no encontrado para el producto en esta lista"
        )
    return {"price": price}