"""
Database Agent - Generación automática de modelos, esquemas y CRUD
"""

import os
import re
from typing import Any, Dict, List
from pathlib import Path
from jinja2 import Template

from ..core import BaseAgent, AgentTask


class DatabaseAgent(BaseAgent):
    """Agente especializado en generación de código de base de datos"""
    
    def __init__(self):
        super().__init__("database_agent", "1.0.0")
        self.backend_path = Path(__file__).parent.parent.parent
        self.models_path = self.backend_path / "app" / "models"
        self.schemas_path = self.backend_path / "app" / "schemas"
        self.crud_path = self.backend_path / "app" / "crud"
    
    def get_capabilities(self) -> List[str]:
        return [
            "generate_model",
            "generate_schema", 
            "generate_crud",
            "generate_migration",
            "analyze_existing_models"
        ]
    
    async def execute(self, task: AgentTask) -> Dict[str, Any]:
        self.start_task(task)
        
        try:
            action = task.parameters.get("action")
            
            if action == "generate_model":
                result = self.generate_model(task.parameters)
            elif action == "generate_schema":
                result = self.generate_schema(task.parameters)
            elif action == "generate_crud":
                result = self.generate_crud(task.parameters)
            elif action == "analyze_models":
                result = self.analyze_existing_models()
            else:
                result = {"success": False, "error": f"Acción '{action}' no soportada"}
            
            self.update_progress(100.0)
            return self.complete_task(result)
            
        except Exception as e:
            self.update_progress(0.0)
            return self.fail_task(str(e))
    
    def generate_model(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar modelo SQLAlchemy"""
        model_name = params.get("model_name")
        table_name = params.get("table_name", f"{model_name.lower()}s")
        fields = params.get("fields", [])
        
        if not model_name:
            return {"success": False, "error": "model_name es requerido"}
        
        # Plantilla de modelo SQLAlchemy
        model_template = Template('''
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class {{ model_name }}(Base):
    __tablename__ = "{{ table_name }}"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
{% for field in fields %}
    {{ field.name }} = Column({{ field.type }}, {{ "nullable=False" if not field.nullable else "nullable=True" }})
{% endfor %}
''')
        
        content = model_template.render(
            model_name=model_name,
            table_name=table_name,
            fields=fields
        )
        
        # Guardar archivo
        file_path = self.models_path / f"{model_name.lower()}.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "model_name": model_name,
            "message": f"Modelo {model_name} generado exitosamente"
        }
    
    def generate_schema(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar esquema Pydantic"""
        schema_name = params.get("schema_name")
        model_name = params.get("model_name", schema_name)
        fields = params.get("fields", [])
        
        if not schema_name:
            return {"success": False, "error": "schema_name es requerido"}
        
        # Plantilla de esquema Pydantic
        schema_template = Template('''
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Schema Base
class {{ schema_name }}Base(BaseModel):
{% for field in fields %}
    {{ field.name }}: {{ field.python_type }}{{ "=" + field.default if field.default else "" }}
{% endfor %}

# Schema para creación
class {{ schema_name }}Create({{ schema_name }}Base):
    pass

# Schema para actualización
class {{ schema_name }}Update(BaseModel):
{% for field in fields %}
    {{ field.name }}: Optional[{{ field.python_type }}] = None
{% endfor %}

# Schema completo (con ID y timestamps)
class {{ schema_name }}({{ schema_name }}Base):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
''')
        
        content = schema_template.render(
            schema_name=schema_name,
            model_name=model_name,
            fields=fields
        )
        
        # Guardar archivo
        file_path = self.schemas_path / f"{schema_name.lower()}.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "schema_name": schema_name,
            "message": f"Esquema {schema_name} generado exitosamente"
        }
    
    def generate_crud(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar funciones CRUD"""
        model_name = params.get("model_name")
        schema_name = params.get("schema_name", model_name)
        
        if not model_name:
            return {"success": False, "error": "model_name es requerido"}
        
        # Plantilla CRUD
        crud_template = Template('''
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.{{ model_name_lower }} import {{ model_name }}
from ..schemas.{{ schema_name_lower }} import {{ schema_name }}Create, {{ schema_name }}Update

def get_{{ model_name_lower }}(db: Session, {{ model_name_lower }}_id: int) -> Optional[{{ model_name }}]:
    return db.query({{ model_name }}).filter({{ model_name }}.id == {{ model_name_lower }}_id).first()

def get_{{ model_name_lower }}s(db: Session, skip: int = 0, limit: int = 100) -> List[{{ model_name }}]:
    return db.query({{ model_name }}).offset(skip).limit(limit).all()

def create_{{ model_name_lower }}(db: Session, {{ model_name_lower }}: {{ schema_name }}Create) -> {{ model_name }}:
    db_{{ model_name_lower }} = {{ model_name }}(**{{ model_name_lower }}.model_dump())
    db.add(db_{{ model_name_lower }})
    db.commit()
    db.refresh(db_{{ model_name_lower }})
    return db_{{ model_name_lower }}

def update_{{ model_name_lower }}(
    db: Session, 
    {{ model_name_lower }}_id: int, 
    {{ model_name_lower }}: {{ schema_name }}Update
) -> Optional[{{ model_name }}]:
    db_{{ model_name_lower }} = db.query({{ model_name }}).filter({{ model_name }}.id == {{ model_name_lower }}_id).first()
    if db_{{ model_name_lower }}:
        update_data = {{ model_name_lower }}.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_{{ model_name_lower }}, key, value)
        db.commit()
        db.refresh(db_{{ model_name_lower }})
    return db_{{ model_name_lower }}

def delete_{{ model_name_lower }}(db: Session, {{ model_name_lower }}_id: int) -> bool:
    db_{{ model_name_lower }} = db.query({{ model_name }}).filter({{ model_name }}.id == {{ model_name_lower }}_id).first()
    if db_{{ model_name_lower }}:
        db.delete(db_{{ model_name_lower }})
        db.commit()
        return True
    return False
''')
        
        content = crud_template.render(
            model_name=model_name,
            model_name_lower=model_name.lower(),
            schema_name=schema_name,
            schema_name_lower=schema_name.lower()
        )
        
        # Guardar archivo
        file_path = self.crud_path / f"{model_name.lower()}.py"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "model_name": model_name,
            "message": f"CRUD para {model_name} generado exitosamente"
        }
    
    def analyze_existing_models(self) -> Dict[str, Any]:
        """Analizar modelos existentes"""
        models = []
        
        for file_path in self.models_path.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Extraer nombre de clase del modelo
                match = re.search(r'class\s+(\w+)\(Base\):', content)
                if match:
                    model_name = match.group(1)
                    
                    # Contar campos
                    field_count = len(re.findall(r'^\s+\w+\s+=\s+Column', content, re.MULTILINE))
                    
                    models.append({
                        "file": file_path.name,
                        "model_name": model_name,
                        "field_count": field_count
                    })
        
        return {
            "success": True,
            "models": models,
            "total": len(models),
            "message": f"Se encontraron {len(models)} modelos"
        }


# Instancia del agente
database_agent = DatabaseAgent()
