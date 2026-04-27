"""
Testing Agent - Generación automática de pruebas unitarias y de integración
"""

import os
from typing import Any, Dict, List
from pathlib import Path
from jinja2 import Template

from ..core import BaseAgent, AgentTask


class TestingAgent(BaseAgent):
    """Agente especializado en generación de pruebas automatizadas"""
    
    def __init__(self):
        super().__init__("testing_agent", "1.0.0")
        self.backend_path = Path(__file__).parent.parent.parent
        self.tests_path = self.backend_path / "tests"
        self.app_path = self.backend_path / "app"
    
    def get_capabilities(self) -> List[str]:
        return [
            "generate_unit_test",
            "generate_integration_test",
            "generate_api_test",
            "generate_test_fixture",
            "analyze_test_coverage"
        ]
    
    async def execute(self, task: AgentTask) -> Dict[str, Any]:
        self.start_task(task)
        
        try:
            action = task.parameters.get("action")
            
            if action == "generate_unit_test":
                result = self.generate_unit_test(task.parameters)
            elif action == "generate_integration_test":
                result = self.generate_integration_test(task.parameters)
            elif action == "generate_api_test":
                result = self.generate_api_test(task.parameters)
            elif action == "generate_fixture":
                result = self.generate_fixture(task.parameters)
            elif action == "analyze_coverage":
                result = self.analyze_test_coverage()
            else:
                result = {"success": False, "error": f"Acción '{action}' no soportada"}
            
            self.update_progress(100.0)
            return self.complete_task(result)
            
        except Exception as e:
            self.update_progress(0.0)
            return self.fail_task(str(e))
    
    def generate_unit_test(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar prueba unitaria"""
        module_name = params.get("module_name")
        function_name = params.get("function_name")
        test_type = params.get("test_type", "success")  # success, error, edge_case
        
        if not module_name:
            return {"success": False, "error": "module_name es requerido"}
        
        test_template = Template('''
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
{% if module_type == "crud" %}
from app.crud.{{ module_name }} import {{ function_name }}
from app.schemas.{{ module_name }} import {{ module_name | capitalize }}Create
{% elif module_type == "service" %}
from app.services.{{ module_name }} import {{ function_name }}
{% endif %}

class Test{{ function_name | capitalize }}:
    \"\"\"Pruebas unitarias para {{ function_name }}\"\"\"
    
    @pytest.fixture
    def mock_db(self):
        \"\"\"Mock de sesión de base de datos\"\"\"
        db = Mock()
        db.query = Mock()
        db.add = Mock()
        db.commit = Mock()
        db.refresh = Mock()
        return db
    
    def test_{{ function_name }}_success(self, mock_db):
        \"\"\"Prueba caso exitoso\"\"\"
        # Arrange
        {% if module_type == "crud" %}
        test_data = {{ module_name | capitalize }}Create(
            name="Test Data",
            is_active=True
        )
        mock_result = Mock()
        mock_result.id = 1
        mock_result.name = "Test Data"
        mock_db.query.return_value.filter.return_value.first.return_value = None
        {% endif %}
        
        # Act
        {% if module_type == "crud" %}
        result = {{ function_name }}(db=mock_db, {{ module_name }}=test_data)
        {% else %}
        result = {{ function_name }}()
        {% endif %}
        
        # Assert
        {% if module_type == "crud" %}
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        {% endif %}
    
    def test_{{ function_name }}_error_handling(self, mock_db):
        \"\"\"Prueba manejo de errores\"\"\"
        # Arrange
        mock_db.commit.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception):
            {% if module_type == "crud" %}
            test_data = {{ module_name | capitalize }}Create(name="Test")
            {{ function_name }}(db=mock_db, {{ module_name }}=test_data)
            {% else %}
            {{ function_name }}()
            {% endif %}
''')
        
        content = test_template.render(
            module_name=module_name,
            function_name=function_name or f"crud_{module_name}",
            module_type=params.get("module_type", "crud"),
            test_type=test_type
        )
        
        # Crear directorio de tests si no existe
        self.tests_path.mkdir(exist_ok=True)
        
        # Guardar archivo
        file_path = self.tests_path / f"test_{module_name}.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "module_name": module_name,
            "message": f"Pruebas unitarias para {module_name} generadas exitosamente"
        }
    
    def generate_integration_test(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar prueba de integración"""
        module_name = params.get("module_name")
        endpoint = params.get("endpoint", f"/{module_name}")
        
        if not module_name:
            return {"success": False, "error": "module_name es requerido"}
        
        integration_template = Template('''
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.{{ module_name }} import {{ module_name | capitalize }}
import json

client = TestClient(app)

class Test{{ module_name | capitalize }}Integration:
    \"\"\"Pruebas de integración para {{ module_name }}\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        \"\"\"Configurar base de datos para pruebas\"\"\"
        # Limpiar datos antes de cada prueba
        yield
        # Limpiar datos después de cada prueba
    
    def test_create_{{ module_name }}(self, auth_headers):
        \"\"\"Prueba creación de {{ module_name }}\"\"\"
        payload = {
            "name": "Test {{ module_name | capitalize }}",
            "is_active": True
        }
        
        response = client.post(
            "{{ endpoint }}/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
        assert "id" in data
    
    def test_get_{{ module_name }}s(self, auth_headers):
        \"\"\"Prueba obtención de lista de {{ module_name }}\"\"\"
        response = client.get(
            "{{ endpoint }}/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_single_{{ module_name }}(self, auth_headers, create_{{ module_name }}):
        \"\"\"Prueba obtención de {{ module_name }} individual\"\"\"
        {{ module_name }} = create_{{ module_name }}
        
        response = client.get(
            f"{{ endpoint }}/{{{{ module_name }}.id}}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == {{ module_name }}.id
    
    def test_update_{{ module_name }}(self, auth_headers, create_{{ module_name }}):
        \"\"\"Prueba actualización de {{ module_name }}\"\"\"
        {{ module_name }} = create_{{ module_name }}
        
        payload = {
            "name": "Updated Name"
        }
        
        response = client.put(
            f"{{ endpoint }}/{{{{ module_name }}.id}}",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
    
    def test_delete_{{ module_name }}(self, auth_headers, create_{{ module_name }}):
        \"\"\"Prueba eliminación de {{ module_name }}\"\"\"
        {{ module_name }} = create_{{ module_name }}
        
        response = client.delete(
            f"{{ endpoint }}/{{{{ module_name }}.id}}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
''')
        
        content = integration_template.render(
            module_name=module_name,
            endpoint=endpoint
        )
        
        # Guardar archivo
        file_path = self.tests_path / f"test_{module_name}_integration.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "module_name": module_name,
            "message": f"Pruebas de integración para {module_name} generadas exitosamente"
        }
    
    def generate_api_test(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar prueba de API específica"""
        endpoint_name = params.get("endpoint_name")
        http_method = params.get("http_method", "GET")
        expected_status = params.get("expected_status", 200)
        
        test_template = Template('''
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_{{ endpoint_name }}_{{ http_method | lower }}():
    \"\"\"Prueba API: {{ http_method }} {{ endpoint_name }}\"\"\"
    {% if http_method == "GET" %}
    response = client.get("{{ endpoint_name }}")
    {% elif http_method == "POST" %}
    response = client.post("{{ endpoint_name }}", json={})
    {% elif http_method == "PUT" %}
    response = client.put("{{ endpoint_name }}", json={})
    {% elif http_method == "DELETE" %}
    response = client.delete("{{ endpoint_name }}")
    {% endif %}
    
    assert response.status_code == {{ expected_status }}
''')
        
        content = test_template.render(
            endpoint_name=endpoint_name,
            http_method=http_method,
            expected_status=expected_status
        )
        
        file_path = self.tests_path / f"test_api_{endpoint_name.replace('/', '_')}.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "endpoint": endpoint_name,
            "message": f"Prueba API para {endpoint_name} generada exitosamente"
        }
    
    def generate_fixture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar fixtures para tests"""
        fixture_name = params.get("fixture_name")
        
        fixture_template = Template('''
import pytest
from datetime import datetime
from app.models.{{ model_name }} import {{ model_name | capitalize }}

@pytest.fixture
def {{ fixture_name }}(db_session):
    \"\"\"Fixture para {{ fixture_name }}\"\"\"
    data = {{ model_name | capitalize }}(
        name="Test {{ model_name | capitalize }}",
        is_active=True,
        created_at=datetime.utcnow()
    )
    db_session.add(data)
    db_session.commit()
    db_session.refresh(data)
    yield data
    db_session.delete(data)
    db_session.commit()
''')
        
        content = fixture_template.render(
            fixture_name=fixture_name,
            model_name=params.get("model_name", fixture_name)
        )
        
        file_path = self.tests_path / "conftest.py"
        
        # Si el archivo ya existe, agregar al final
        if file_path.exists():
            with open(file_path, 'a') as f:
                f.write("\n\n" + content)
        else:
            with open(file_path, 'w') as f:
                f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "fixture_name": fixture_name,
            "message": f"Fixture {fixture_name} generado exitosamente"
        }
    
    def analyze_test_coverage(self) -> Dict[str, Any]:
        """Analizar cobertura de tests existente"""
        test_files = list(self.tests_path.glob("test_*.py"))
        
        modules_tested = []
        for file_path in test_files:
            with open(file_path, 'r') as f:
                content = f.read()
                test_count = content.count("def test_")
                modules_tested.append({
                    "file": file_path.name,
                    "test_count": test_count
                })
        
        total_tests = sum(m["test_count"] for m in modules_tested)
        
        return {
            "success": True,
            "test_files": len(test_files),
            "total_tests": total_tests,
            "modules": modules_tested,
            "message": f"Se encontraron {total_tests} pruebas en {len(test_files)} archivos"
        }


# Instancia del agente
testing_agent = TestingAgent()
