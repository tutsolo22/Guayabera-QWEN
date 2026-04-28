"""
Size Chart API Router: Standard Mexican sizing for clothing
Including sizes for men, women, boys, girls with standard measurements
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.size_chart import (
    TablaTallaCreate, TablaTallaUpdate, TablaTallaResponse,
    TallaCreate, TallaUpdate, TallaResponse,
    ReferenciaTallaCreate, ReferenciaTallaUpdate, ReferenciaTallaResponse
)
from app.crud.size_chart import (
    create_tabla_talla, get_tabla_talla, get_tabla_talla_by_codigo,
    get_tablas_talla, update_tabla_talla, delete_tabla_talla,
    create_talla, get_talla, get_tallas_by_tabla_talla, get_talla_by_codigo,
    update_talla, delete_talla,
    create_referencia_talla, get_referencia_talla, get_referencias_by_talla,
    update_referencia_talla, delete_referencia_talla
)

router = APIRouter(prefix="/size-chart", tags=["Size Charts"])

# ============================================================================
# SIZE CHART ENDPOINTS
# ============================================================================

@router.post("/tables/", response_model=TablaTallaResponse)
def create_size_chart(tabla: TablaTallaCreate, db: Session = Depends(get_db)):
    """Create a new size chart"""
    # Check if chart code already exists
    existing_tabla = get_tabla_talla_by_codigo(db, tabla.codigo)
    if existing_tabla:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Size chart with this code already exists"
        )
    
    return create_tabla_talla(db=db, tabla_data=tabla)


@router.get("/tables/{tabla_id}", response_model=TablaTallaResponse)
def get_size_chart(tabla_id: str, db: Session = Depends(get_db)):
    """Get a size chart by ID"""
    tabla = get_tabla_talla(db, tabla_id)
    if not tabla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size chart not found"
        )
    return tabla


@router.get("/tables/", response_model=List[TablaTallaResponse])
def get_size_charts(
    skip: int = 0, 
    limit: int = 100,
    activa: Optional[bool] = None,
    tipo_prenda: Optional[str] = None,
    genero: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of size charts, optionally filtered"""
    return get_tablas_talla(
        db, 
        skip=skip, 
        limit=limit, 
        activa=activa, 
        tipo_prenda=tipo_prenda,
        genero=genero
    )


@router.put("/tables/{tabla_id}", response_model=TablaTallaResponse)
def update_size_chart(
    tabla_id: str, 
    tabla_data: TablaTallaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a size chart"""
    updated_tabla = update_tabla_talla(
        db=db, 
        tabla_id=tabla_id, 
        tabla_data=tabla_data
    )
    if not updated_tabla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size chart not found"
        )
    return updated_tabla


@router.delete("/tables/{tabla_id}")
def delete_size_chart(tabla_id: str, db: Session = Depends(get_db)):
    """Delete a size chart"""
    success = delete_tabla_talla(db=db, tabla_id=tabla_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size chart not found"
        )
    return {"message": "Size chart deleted successfully"}


# ============================================================================
# SIZE ENDPOINTS
# ============================================================================

@router.post("/sizes/", response_model=TallaResponse)
def create_size(talla: TallaCreate, db: Session = Depends(get_db)):
    """Create a new size"""
    return create_talla(db=db, talla_data=talla)


@router.get("/sizes/{talla_id}", response_model=TallaResponse)
def get_size(talla_id: str, db: Session = Depends(get_db)):
    """Get a size by ID"""
    talla = get_talla(db, talla_id)
    if not talla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found"
        )
    return talla


@router.get("/tables/{tabla_talla_id}/sizes", response_model=List[TallaResponse])
def get_sizes_by_chart(tabla_talla_id: str, db: Session = Depends(get_db)):
    """Get all sizes for a specific size chart"""
    return get_tallas_by_tabla_talla(db, tabla_talla_id)


@router.get("/tables/{tabla_talla_id}/sizes/{codigo}", response_model=TallaResponse)
def get_size_by_code(tabla_talla_id: str, codigo: str, db: Session = Depends(get_db)):
    """Get a size by code within a specific chart"""
    talla = get_talla_by_codigo(db, tabla_talla_id, codigo)
    if not talla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found in this chart"
        )
    return talla


@router.put("/sizes/{talla_id}", response_model=TallaResponse)
def update_size(
    talla_id: str, 
    talla_data: TallaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a size"""
    updated_talla = update_talla(
        db=db, 
        talla_id=talla_id, 
        talla_data=talla_data
    )
    if not updated_talla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found"
        )
    return updated_talla


@router.delete("/sizes/{talla_id}")
def delete_size(talla_id: str, db: Session = Depends(get_db)):
    """Delete a size"""
    success = delete_talla(db=db, talla_id=talla_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found"
        )
    return {"message": "Size deleted successfully"}


# ============================================================================
# SIZE REFERENCE ENDPOINTS
# ============================================================================

@router.post("/references/", response_model=ReferenciaTallaResponse)
def create_size_reference(referencia: ReferenciaTallaCreate, db: Session = Depends(get_db)):
    """Create a new size reference"""
    return create_referencia_talla(db=db, referencia_data=referencia)


@router.get("/references/{referencia_id}", response_model=ReferenciaTallaResponse)
def get_size_reference(referencia_id: str, db: Session = Depends(get_db)):
    """Get a size reference by ID"""
    referencia = get_referencia_talla(db, referencia_id)
    if not referencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size reference not found"
        )
    return referencia


@router.get("/sizes/{talla_id}/references", response_model=List[ReferenciaTallaResponse])
def get_size_references(talla_id: str, db: Session = Depends(get_db)):
    """Get all references for a specific size"""
    return get_referencias_by_talla(db, talla_id)


@router.put("/references/{referencia_id}", response_model=ReferenciaTallaResponse)
def update_size_reference(
    referencia_id: str, 
    referencia_data: ReferenciaTallaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a size reference"""
    updated_referencia = update_referencia_talla(
        db=db, 
        referencia_id=referencia_id, 
        referencia_data=referencia_data
    )
    if not updated_referencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size reference not found"
        )
    return updated_referencia


@router.delete("/references/{referencia_id}")
def delete_size_reference(referencia_id: str, db: Session = Depends(get_db)):
    """Delete a size reference"""
    success = delete_referencia_talla(db=db, referencia_id=referencia_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size reference not found"
        )
    return {"message": "Size reference deleted successfully"}