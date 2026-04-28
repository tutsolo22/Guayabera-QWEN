"""
CAD Integration API Router: Designs, patterns, and technical sheets
Specialized for textile manufacturing companies
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.cad import (
    DisenoCreate, DisenoUpdate, DisenoResponse,
    DisenoTallaCreate, DisenoTallaUpdate, DisenoTallaResponse,
    ComponenteDisenoCreate, ComponenteDisenoUpdate, ComponenteDisenoResponse,
    FichaTecnicaCreate, FichaTecnicaUpdate, FichaTecnicaResponse,
    HistoricoDisenoCreate, HistoricoDisenoResponse
)
from app.crud.cad import (
    create_diseno, get_diseno, get_diseno_by_codigo,
    get_diseños, update_diseno, delete_diseno,
    create_diseno_talla, get_diseno_talla, get_diseños_tallas_by_diseno,
    update_diseno_talla, delete_diseno_talla,
    create_componente_diseno, get_componente_diseno, get_componentes_by_diseno,
    update_componente_diseno, delete_componente_diseno,
    create_ficha_tecnica, get_ficha_tecnica, get_ficha_tecnica_by_codigo,
    get_fichas_tecnicas_by_diseno, update_ficha_tecnica, delete_ficha_tecnica,
    create_historico_diseno, get_historico_diseno, get_historicos_by_diseno
)

router = APIRouter(prefix="/cad", tags=["CAD Design"])

# ============================================================================
# DESIGN ENDPOINTS
# ============================================================================

@router.post("/designs/", response_model=DisenoResponse)
def create_design(diseno: DisenoCreate, db: Session = Depends(get_db)):
    """Create a new design"""
    # Check if design code already exists
    existing_diseno = get_diseno_by_codigo(db, diseno.codigo)
    if existing_diseno:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Design with this code already exists"
        )
    
    return create_diseno(db=db, diseno_data=diseno)


@router.get("/designs/{diseno_id}", response_model=DisenoResponse)
def get_design(diseno_id: str, db: Session = Depends(get_db)):
    """Get a design by ID"""
    diseno = get_diseno(db, diseno_id)
    if not diseno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    return diseno


@router.get("/designs/", response_model=List[DisenoResponse])
def get_designs(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    tipo_diseno: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of designs, optionally filtered"""
    return get_diseños(
        db, 
        skip=skip, 
        limit=limit, 
        activo=activo, 
        tipo_diseno=tipo_diseno
    )


@router.put("/designs/{diseno_id}", response_model=DisenoResponse)
def update_design(
    diseno_id: str, 
    diseno_data: DisenoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a design"""
    updated_diseno = update_diseno(
        db=db, 
        diseno_id=diseno_id, 
        diseno_data=diseno_data
    )
    if not updated_diseno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    return updated_diseno


@router.delete("/designs/{diseno_id}")
def delete_design(diseno_id: str, db: Session = Depends(get_db)):
    """Delete a design"""
    success = delete_diseno(db=db, diseno_id=diseno_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    return {"message": "Design deleted successfully"}


# ============================================================================
# DESIGN SIZE SPECIFICATION ENDPOINTS
# ============================================================================

@router.post("/design-sizes/", response_model=DisenoTallaResponse)
def create_design_size(diseno_talla: DisenoTallaCreate, db: Session = Depends(get_db)):
    """Create a new design size specification"""
    return create_diseno_talla(db=db, diseno_talla_data=diseno_talla)


@router.get("/design-sizes/{diseno_talla_id}", response_model=DisenoTallaResponse)
def get_design_size(diseno_talla_id: str, db: Session = Depends(get_db)):
    """Get a design size specification by ID"""
    diseno_talla = get_diseno_talla(db, diseno_talla_id)
    if not diseno_talla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design size specification not found"
        )
    return diseno_talla


@router.get("/designs/{diseno_id}/sizes", response_model=List[DisenoTallaResponse])
def get_design_sizes(diseno_id: str, db: Session = Depends(get_db)):
    """Get all size specifications for a specific design"""
    return get_diseños_tallas_by_diseno(db, diseno_id)


@router.put("/design-sizes/{diseno_talla_id}", response_model=DisenoTallaResponse)
def update_design_size(
    diseno_talla_id: str, 
    diseno_talla_data: DisenoTallaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a design size specification"""
    updated_diseno_talla = update_diseno_talla(
        db=db, 
        diseno_talla_id=diseno_talla_id, 
        diseno_talla_data=diseno_talla_data
    )
    if not updated_diseno_talla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design size specification not found"
        )
    return updated_diseno_talla


@router.delete("/design-sizes/{diseno_talla_id}")
def delete_design_size(diseno_talla_id: str, db: Session = Depends(get_db)):
    """Delete a design size specification"""
    success = delete_diseno_talla(db=db, diseno_talla_id=diseno_talla_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design size specification not found"
        )
    return {"message": "Design size specification deleted successfully"}


# ============================================================================
# DESIGN COMPONENT ENDPOINTS
# ============================================================================

@router.post("/components/", response_model=ComponenteDisenoResponse)
def create_design_component(componente: ComponenteDisenoCreate, db: Session = Depends(get_db)):
    """Create a new design component"""
    return create_componente_diseno(db=db, componente_data=componente)


@router.get("/components/{componente_id}", response_model=ComponenteDisenoResponse)
def get_design_component(componente_id: str, db: Session = Depends(get_db)):
    """Get a design component by ID"""
    componente = get_componente_diseno(db, componente_id)
    if not componente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design component not found"
        )
    return componente


@router.get("/designs/{diseno_id}/components", response_model=List[ComponenteDisenoResponse])
def get_design_components(diseno_id: str, db: Session = Depends(get_db)):
    """Get all components for a specific design"""
    return get_componentes_by_diseno(db, diseno_id)


@router.put("/components/{componente_id}", response_model=ComponenteDisenoResponse)
def update_design_component(
    componente_id: str, 
    componente_data: ComponenteDisenoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a design component"""
    updated_componente = update_componente_diseno(
        db=db, 
        componente_id=componente_id, 
        componente_data=componente_data
    )
    if not updated_componente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design component not found"
        )
    return updated_componente


@router.delete("/components/{componente_id}")
def delete_design_component(componente_id: str, db: Session = Depends(get_db)):
    """Delete a design component"""
    success = delete_componente_diseno(db=db, componente_id=componente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design component not found"
        )
    return {"message": "Design component deleted successfully"}


# ============================================================================
# TECHNICAL SHEET ENDPOINTS
# ============================================================================

@router.post("/technical-sheets/", response_model=FichaTecnicaResponse)
def create_technical_sheet(ficha: FichaTecnicaCreate, db: Session = Depends(get_db)):
    """Create a new technical sheet"""
    try:
        return create_ficha_tecnica(db=db, ficha_data=ficha)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/technical-sheets/{ficha_id}", response_model=FichaTecnicaResponse)
def get_technical_sheet(ficha_id: str, db: Session = Depends(get_db)):
    """Get a technical sheet by ID"""
    ficha = get_ficha_tecnica(db, ficha_id)
    if not ficha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technical sheet not found"
        )
    return ficha


@router.get("/technical-sheets/code/{codigo}", response_model=FichaTecnicaResponse)
def get_technical_sheet_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a technical sheet by code"""
    ficha = get_ficha_tecnica_by_codigo(db, codigo)
    if not ficha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technical sheet not found"
        )
    return ficha


@router.get("/designs/{diseno_id}/technical-sheets", response_model=List[FichaTecnicaResponse])
def get_design_technical_sheets(diseno_id: str, db: Session = Depends(get_db)):
    """Get all technical sheets for a specific design"""
    return get_fichas_tecnicas_by_diseno(db, diseno_id)


@router.put("/technical-sheets/{ficha_id}", response_model=FichaTecnicaResponse)
def update_technical_sheet(
    ficha_id: str, 
    ficha_data: FichaTecnicaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a technical sheet"""
    updated_ficha = update_ficha_tecnica(
        db=db, 
        ficha_id=ficha_id, 
        ficha_data=ficha_data
    )
    if not updated_ficha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technical sheet not found"
        )
    return updated_ficha


@router.delete("/technical-sheets/{ficha_id}")
def delete_technical_sheet(ficha_id: str, db: Session = Depends(get_db)):
    """Delete a technical sheet"""
    success = delete_ficha_tecnica(db=db, ficha_id=ficha_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technical sheet not found"
        )
    return {"message": "Technical sheet deleted successfully"}


# ============================================================================
# DESIGN HISTORY ENDPOINTS
# ============================================================================

@router.post("/history/", response_model=HistoricoDisenoResponse)
def create_design_history(historico: HistoricoDisenoCreate, db: Session = Depends(get_db)):
    """Create a new design history entry"""
    return create_historico_diseno(db=db, historico_data=historico)


@router.get("/history/{historico_id}", response_model=HistoricoDisenoResponse)
def get_design_history(historico_id: str, db: Session = Depends(get_db)):
    """Get a design history entry by ID"""
    historico = get_historico_diseno(db, historico_id)
    if not historico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design history entry not found"
        )
    return historico


@router.get("/designs/{diseno_id}/history", response_model=List[HistoricoDisenoResponse])
def get_design_history_entries(diseno_id: str, db: Session = Depends(get_db)):
    """Get all history entries for a specific design"""
    return get_historicos_by_diseno(db, diseno_id)