"""
Tests for Supply Chain Module
Purchases, Suppliers, Inventory, Warehouse
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from app.main import app
from app.core.database import Base, get_db
from app.models.supply_chain import (
    Proveedor, Producto, Almacen, OrdenCompra, 
    EstadoOrdenCompra, TipoProveedor
)
from app.schemas.supply_chain import (
    ProveedorCreate, ProductoCreate, AlmacenCreate,
    OrdenCompraCreate, OrdenCompraDetalleCreate
)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with overridden database dependency"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client, db_session):
    """Get authentication headers for testing"""
    # First, we need to create a test user and get a token
    # For now, we'll skip authentication in some tests
    return {"Authorization": "Bearer test_token"}


class TestProveedor:
    """Test suite for Supplier endpoints"""
    
    def test_crear_proveedor(self, client, db_session, auth_headers):
        """Test creating a new supplier"""
        proveedor_data = {
            "codigo": "PROV001",
            "nombre_comercial": "Proveedor de Telas SA",
            "razon_social": "Proveedor de Telas Sociedad Anónima",
            "rfc": "PTS900101ABC",
            "regimen_fiscal": "601 - General de Ley Personas Morales",
            "correo_electronico": "contacto@proveedor.com",
            "telefono": "9991234567",
            "tipo_proveedor": "nacional",
            "credito_maximo": "50000.00",
            "dias_credito": 30,
            "activo": True
        }
        
        response = client.post(
            "/api/v1/supply-chain/proveedores",
            json=proveedor_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["codigo"] == "PROV001"
        assert data["nombre_comercial"] == "Proveedor de Telas SA"
        assert data["rfc"] == "PTS900101ABC"
        assert "id" in data
    
    def test_listar_proveedores(self, client, db_session):
        """Test listing all suppliers"""
        # Create test data
        proveedor = Proveedor(
            codigo="PROV002",
            nombre_comercial="Otro Proveedor",
            rfc="OPR900101XYZ",
            activo=True
        )
        db_session.add(proveedor)
        db_session.commit()
        
        response = client.get("/api/v1/supply-chain/proveedores")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_obtener_proveedor(self, client, db_session):
        """Test getting a specific supplier"""
        proveedor = Proveedor(
            codigo="PROV003",
            nombre_comercial="Proveedor Específico",
            rfc="PE900101ABC",
            activo=True
        )
        db_session.add(proveedor)
        db_session.commit()
        
        response = client.get(f"/api/v1/supply-chain/proveedores/{proveedor.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(proveedor.id)
        assert data["nombre_comercial"] == "Proveedor Específico"
    
    def test_proveedor_rfc_duplicado(self, client, db_session, auth_headers):
        """Test that duplicate RFC is rejected"""
        proveedor_data = {
            "codigo": "PROV004",
            "nombre_comercial": "Proveedor Duplicado",
            "rfc": "DUP900101ABC",
            "activo": True
        }
        
        # Create first supplier
        response1 = client.post(
            "/api/v1/supply-chain/proveedores",
            json=proveedor_data,
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post(
            "/api/v1/supply-chain/proveedores",
            json=proveedor_data,
            headers=auth_headers
        )
        
        assert response2.status_code == 400
        assert "ya está registrado" in response2.json()["detail"]


class TestProducto:
    """Test suite for Product endpoints"""
    
    def test_crear_producto(self, client, db_session, auth_headers):
        """Test creating a new product"""
        producto_data = {
            "codigo": "PROD001",
            "nombre": "Guayabera Blanca Talla M",
            "descripcion": "Guayabera tradicional blanca",
            "clave_sat": "10101602",
            "unidad_medida": "Pieza",
            "costo_promedio": "250.00",
            "precio_venta_base": "450.00",
            "stock_minimo": 10,
            "activo": True
        }
        
        response = client.post(
            "/api/v1/supply-chain/productos",
            json=producto_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["codigo"] == "PROD001"
        assert data["nombre"] == "Guayabera Blanca Talla M"
        assert float(data["precio_venta_base"]) == 450.00
    
    def test_listar_productos(self, client, db_session):
        """Test listing products"""
        producto = Producto(
            codigo="PROD002",
            nombre="Camisa Casual",
            costo_promedio=Decimal("200.00"),
            precio_venta_base=Decimal("350.00"),
            activo=True
        )
        db_session.add(producto)
        db_session.commit()
        
        response = client.get("/api/v1/supply-chain/productos")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestAlmacen:
    """Test suite for Warehouse endpoints"""
    
    def test_crear_almacen(self, client, db_session, auth_headers):
        """Test creating a new warehouse"""
        almacen_data = {
            "codigo": "ALM001",
            "nombre": "Almacén Principal",
            "descripcion": "Almacén central de Mérida",
            "ciudad": "Mérida",
            "estado": "Yucatán",
            "tipo": "general",
            "es_principal": True,
            "activo": True
        }
        
        response = client.post(
            "/api/v1/supply-chain/almacenes",
            json=almacen_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["codigo"] == "ALM001"
        assert data["nombre"] == "Almacén Principal"
        assert data["es_principal"] == True


class TestOrdenCompra:
    """Test suite for Purchase Order endpoints"""
    
    def test_crear_orden_compra(self, client, db_session, auth_headers):
        """Test creating a purchase order"""
        # First create supplier and product
        proveedor = Proveedor(
            codigo="PROV005",
            nombre_comercial="Proveedor para OC",
            rfc="POC900101ABC",
            activo=True
        )
        db_session.add(proveedor)
        
        producto = Producto(
            codigo="PROD003",
            nombre="Producto para OC",
            costo_promedio=Decimal("100.00"),
            precio_venta_base=Decimal("150.00"),
            activo=True
        )
        db_session.add(producto)
        
        almacen = Almacen(
            codigo="ALM002",
            nombre="Almacén para OC",
            activo=True
        )
        db_session.add(almacen)
        db_session.commit()
        
        orden_data = {
            "proveedor_id": str(proveedor.id),
            "fecha_emision": str(date.today()),
            "almacen_id": str(almacen.id),
            "detalles": [
                {
                    "producto_id": str(producto.id),
                    "cantidad_pedida": "10.00",
                    "costo_unitario": "100.00",
                    "descuento_porcentaje": "0.00",
                    "iva_porcentaje": "16.00"
                }
            ]
        }
        
        response = client.post(
            "/api/v1/supply-chain/ordenes-compra",
            json=orden_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "folio" in data
        assert data["estado"] == "borrador"


class TestInventario:
    """Test suite for Inventory endpoints"""
    
    def test_listar_inventarios(self, client, db_session):
        """Test listing inventories"""
        response = client.get("/api/v1/supply-chain/inventarios")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_dashboard_inventario(self, client, db_session):
        """Test inventory dashboard endpoint"""
        response = client.get("/api/v1/supply-chain/dashboard/inventario")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_productos" in data
        assert "productos_activos" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
