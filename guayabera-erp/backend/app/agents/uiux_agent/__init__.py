"""
UI/UX Agent - Generación de componentes React y páginas
"""

import os
from typing import Any, Dict, List
from pathlib import Path
from jinja2 import Template

from ..core import BaseAgent, AgentTask


class UIUXAgent(BaseAgent):
    """Agente especializado en generación de componentes UI/UX"""
    
    def __init__(self):
        super().__init__("uiux_agent", "1.0.0")
        self.frontend_path = Path(__file__).parent.parent.parent.parent / "frontend"
        self.components_path = self.frontend_path / "src" / "components"
        self.pages_path = self.frontend_path / "src" / "pages"
        self.services_path = self.frontend_path / "src" / "services"
    
    def get_capabilities(self) -> List[str]:
        return [
            "generate_component",
            "generate_page",
            "generate_service",
            "generate_form",
            "generate_table",
            "analyze_ui_structure"
        ]
    
    async def execute(self, task: AgentTask) -> Dict[str, Any]:
        self.start_task(task)
        
        try:
            action = task.parameters.get("action")
            
            if action == "generate_component":
                result = self.generate_component(task.parameters)
            elif action == "generate_page":
                result = self.generate_page(task.parameters)
            elif action == "generate_service":
                result = self.generate_service(task.parameters)
            elif action == "generate_form":
                result = self.generate_form(task.parameters)
            elif action == "generate_table":
                result = self.generate_table(task.parameters)
            elif action == "analyze_ui":
                result = self.analyze_ui_structure()
            else:
                result = {"success": False, "error": f"Acción '{action}' no soportada"}
            
            self.update_progress(100.0)
            return self.complete_task(result)
            
        except Exception as e:
            self.update_progress(0.0)
            return self.fail_task(str(e))
    
    def generate_component(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar componente React"""
        component_name = params.get("component_name")
        component_type = params.get("component_type", "functional")  # functional, class
        has_props = params.get("has_props", True)
        has_state = params.get("has_state", False)
        
        if not component_name:
            return {"success": False, "error": "component_name es requerido"}
        
        component_template = Template('''
import React from 'react';
{% if has_state %}
import { useState, useEffect } from 'react';
{% endif %}
import { {{ antd_components | default('Button, Card') }} } from 'antd';
{% if has_props %}
interface {{ component_name }}Props {
  {% for prop in props %}
  {{ prop.name }}: {{ prop.type }}{{ prop.optional ? '?' : '' }};
  {% endfor %}
}
{% endif %}

const {{ component_name }}: React.FC<{{ component_name }}Props> = ({% if has_props %}props{% endif %}) => {
  {% if has_state %}
  const [state, setState] = useState<any>(null);
  {% endif %}

  {% if has_state %}
  useEffect(() => {
    // Lógica de inicialización
  }, []);
  {% endif %}

  const handleAction = () => {
    // Lógica del componente
  };

  return (
    <div className="{{ component_name | lower }}-container">
      <Card title="{{ component_name | replace('_', ' ') }}">
        {/* Contenido del componente */}
        <Button type="primary" onClick={handleAction}>
          Acción
        </Button>
      </Card>
    </div>
  );
};

export default {{ component_name }};
''')
        
        content = component_template.render(
            component_name=component_name,
            component_type=component_type,
            has_props=has_props,
            has_state=has_state,
            props=params.get("props", []),
            antd_components=params.get("antd_components", "Button, Card")
        )
        
        # Crear directorio si no existe
        component_dir = self.components_path / component_name
        component_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        file_path = component_dir / "index.tsx"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "component_name": component_name,
            "message": f"Componente {component_name} generado exitosamente"
        }
    
    def generate_page(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar página React"""
        page_name = params.get("page_name")
        has_crud = params.get("has_crud", True)
        api_endpoint = params.get("api_endpoint", "")
        
        if not page_name:
            return {"success": False, "error": "page_name es requerido"}
        
        page_template = Template('''
import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Modal, Form, Input, message, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
{% if api_endpoint %}
import { {{ page_name }}Service } from '../../services/{{ page_name | lower }}';
{% endif %}

interface {{ page_name | capitalize }}Data {
  id: number;
  name: string;
  is_active: boolean;
  created_at: string;
}

const {{ page_name | capitalize }}Page: React.FC = () => {
  const [data, setData] = useState<{{ page_name | capitalize }}Data[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingItem, setEditingItem] = useState<{{ page_name | capitalize }}Data | null>(null);
  const [form] = Form.useForm();

  // Cargar datos
  const loadData = async () => {
    setLoading(true);
    try {
      {% if api_endpoint %}
      const response = await {{ page_name }}Service.getAll();
      setData(response);
      {% else %}
      // TODO: Implementar llamada a API
      {% endif %}
    } catch (error) {
      message.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Manejar creación/edición
  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      {% if api_endpoint %}
      if (editingItem) {
        await {{ page_name }}Service.update(editingItem.id, values);
      } else {
        await {{ page_name }}Service.create(values);
      }
      {% endif %}
      message.success(editingItem ? 'Actualizado exitosamente' : 'Creado exitosamente');
      setModalVisible(false);
      form.resetFields();
      setEditingItem(null);
      loadData();
    } catch (error) {
      message.error('Error al guardar');
    }
  };

  // Manejar eliminación
  const handleDelete = async (id: number) => {
    try {
      {% if api_endpoint %}
      await {{ page_name }}Service.delete(id);
      {% endif %}
      message.success('Eliminado exitosamente');
      loadData();
    } catch (error) {
      message.error('Error al eliminar');
    }
  };

  // Columnas de la tabla
  const columns: ColumnsType<{{ page_name | capitalize }}Data> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Estado',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active ? 'Activo' : 'Inactivo',
    },
    {
      title: 'Fecha Creación',
      dataIndex: 'created_at',
      key: 'created_at',
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => {
              setEditingItem(record);
              form.setFieldsValue(record);
              setModalVisible(true);
            }}
          />
          <Popconfirm
            title="¿Está seguro de eliminar?"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button type="link" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="{{ page_name | lower }}-page">
      <div style={{ marginBottom: 16 }}>
        <Space>
          <h1>{{ page_name | replace('_', ' ') | capitalize }}</h1>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingItem(null);
              form.resetFields();
              setModalVisible(true);
            }}
          >
            Nuevo
          </Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        rowKey="id"
      />

      <Modal
        title={editingItem ? 'Editar' : 'Nuevo'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setEditingItem(null);
        }}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Nombre"
            rules={[{ required: true, message: 'Por favor ingrese el nombre' }]}
          >
            <Input />
          </Form.Item>
          {/* Agregar más campos según sea necesario */}
        </Form>
      </Modal>
    </div>
  );
};

export default {{ page_name | capitalize }}Page;
''')
        
        content = page_template.render(
            page_name=page_name,
            has_crud=has_crud,
            api_endpoint=api_endpoint
        )
        
        # Crear directorio si no existe
        page_dir = self.pages_path / page_name
        page_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        file_path = page_dir / "index.tsx"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "page_name": page_name,
            "message": f"Página {page_name} generada exitosamente"
        }
    
    def generate_service(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar servicio API"""
        service_name = params.get("service_name")
        api_base_url = params.get("api_base_url", "/api/v1")
        endpoints = params.get("endpoints", [])
        
        if not service_name:
            return {"success": False, "error": "service_name es requerido"}
        
        service_template = Template('''
import api from './api';

export interface {{ service_name | capitalize }}Create {
  name: string;
  is_active?: boolean;
}

export interface {{ service_name | capitalize }}Update {
  name?: string;
  is_active?: boolean;
}

export interface {{ service_name | capitalize }}Response {
  id: number;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

class {{ service_name | capitalize }}Service {
  private baseUrl = '{{ api_base_url }}/{{ service_name | lower }}';

  async getAll(params?: any): Promise<{{ service_name | capitalize }}Response[]> {
    const response = await api.get(this.baseUrl, { params });
    return response.data;
  }

  async getById(id: number): Promise<{{ service_name | capitalize }}Response> {
    const response = await api.get(`${this.baseUrl}/${id}`);
    return response.data;
  }

  async create(data: {{ service_name | capitalize }}Create): Promise<{{ service_name | capitalize }}Response> {
    const response = await api.post(this.baseUrl, data);
    return response.data;
  }

  async update(id: number, data: {{ service_name | capitalize }}Update): Promise<{{ service_name | capitalize }}Response> {
    const response = await api.put(`${this.baseUrl}/${id}`, data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await api.delete(`${this.baseUrl}/${id}`);
  }
}

export const {{ service_name | lower }}Service = new {{ service_name | capitalize }}Service();
''')
        
        content = service_template.render(
            service_name=service_name,
            api_base_url=api_base_url,
            endpoints=endpoints
        )
        
        # Guardar archivo
        file_path = self.services_path / f"{service_name.lower()}.ts"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "service_name": service_name,
            "message": f"Servicio {service_name} generado exitosamente"
        }
    
    def generate_form(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar formulario React"""
        form_name = params.get("form_name")
        fields = params.get("fields", [])
        
        if not form_name:
            return {"success": False, "error": "form_name es requerido"}
        
        form_template = Template('''
import React from 'react';
import { Form, Input, Select, DatePicker, Checkbox, Button } from 'antd';
import type { FormProps } from 'antd';

interface {{ form_name | capitalize }}Values {
{% for field in fields %}
  {{ field.name }}: {{ field.type | default('string') }};
{% endfor %}
}

interface {{ form_name | capitalize }}FormProps {
  initialValues?: Partial<{{ form_name | capitalize }}Values>;
  onSubmit: (values: {{ form_name | capitalize }}Values) => void;
  loading?: boolean;
}

const {{ form_name | capitalize }}Form: React.FC<{{ form_name | capitalize }}FormProps> = ({
  initialValues,
  onSubmit,
  loading = false,
}) => {
  const [form] = Form.useForm<{{ form_name | capitalize }}Values>();

  const onFinish: FormProps<{{ form_name | capitalize }}Values>['onFinish'] = (values) => {
    onSubmit(values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      initialValues={initialValues}
      onFinish={onFinish}
    >
{% for field in fields %}
      <Form.Item
        name="{{ field.name }}"
        label="{{ field.label | default(field.name) }}"
        {% if field.required %}rules={[{ required: true, message: 'Por favor ingrese {{ field.label | default(field.name) }}' }]}{% endif %}
      >
        {% if field.type == 'string' %}
        <Input />
        {% elif field.type == 'number' %}
        <Input type="number" />
        {% elif field.type == 'boolean' %}
        <Checkbox />
        {% elif field.type == 'date' %}
        <DatePicker />
        {% elif field.type == 'select' %}
        <Select>
          {% for option in field.options %}
          <Select.Option value="{{ option.value }}">{{ option.label }}</Select.Option>
          {% endfor %}
        </Select>
        {% endif %}
      </Form.Item>
{% endfor %}
      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            Guardar
          </Button>
          <Button htmlType="reset">Cancelar</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default {{ form_name | capitalize }}Form;
''')
        
        content = form_template.render(
            form_name=form_name,
            fields=fields
        )
        
        # Crear directorio si no existe
        form_dir = self.components_path / f"{form_name}Form"
        form_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        file_path = form_dir / "index.tsx"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "form_name": form_name,
            "message": f"Formulario {form_name} generado exitosamente"
        }
    
    def generate_table(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar tabla React con Ant Design"""
        table_name = params.get("table_name")
        columns = params.get("columns", [])
        has_actions = params.get("has_actions", True)
        
        if not table_name:
            return {"success": False, "error": "table_name es requerido"}
        
        table_template = Template('''
import React from 'react';
import { Table, Space, Button, Popconfirm } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface {{ table_name | capitalize }}Data {
  id: number;
{% for column in columns %}
  {{ column.key }}: {{ column.type | default('string') }};
{% endfor %}
}

interface {{ table_name | capitalize }}TableProps {
  data: {{ table_name | capitalize }}Data[];
  loading?: boolean;
  onEdit?: (record: {{ table_name | capitalize }}Data) => void;
  onDelete?: (id: number) => void;
}

const {{ table_name | capitalize }}Table: React.FC<{{ table_name | capitalize }}TableProps> = ({
  data,
  loading = false,
  onEdit,
  onDelete,
}) => {
  const columns: ColumnsType<{{ table_name | capitalize }}Data> = [
{% for column in columns %}
    {
      title: '{{ column.title | default(column.key) }}',
      dataIndex: '{{ column.key }}',
      key: '{{ column.key }}',
      {% if column.width %}width: {{ column.width }},{% endif %}
      {% if column.render %}render: {{ column.render }},{% endif %}
    },
{% endfor %}
{% if has_actions %}
    {
      title: 'Acciones',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          {onEdit && (
            <Button
              type="link"
              icon={<EditOutlined />}
              onClick={() => onEdit(record)}
            />
          )}
          {onDelete && (
            <Popconfirm
              title="¿Está seguro de eliminar?"
              onConfirm={() => onDelete(record.id)}
            >
              <Button type="link" danger icon={<DeleteOutlined />} />
            </Popconfirm>
          )}
        </Space>
      ),
    },
{% endif %}
  ];

  return (
    <Table
      columns={columns}
      dataSource={data}
      loading={loading}
      rowKey="id"
    />
  );
};

export default {{ table_name | capitalize }}Table;
''')
        
        content = table_template.render(
            table_name=table_name,
            columns=columns,
            has_actions=has_actions
        )
        
        # Crear directorio si no existe
        table_dir = self.components_path / f"{table_name}Table"
        table_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        file_path = table_dir / "index.tsx"
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file": str(file_path),
            "table_name": table_name,
            "message": f"Tabla {table_name} generada exitosamente"
        }
    
    def analyze_ui_structure(self) -> Dict[str, Any]:
        """Analizar estructura UI existente"""
        components = []
        pages = []
        
        # Analizar componentes
        if self.components_path.exists():
            for item in self.components_path.iterdir():
                if item.is_dir():
                    component_file = item / "index.tsx"
                    if component_file.exists():
                        components.append(item.name)
        
        # Analizar páginas
        if self.pages_path.exists():
            for item in self.pages_path.iterdir():
                if item.is_dir():
                    page_file = item / "index.tsx"
                    if page_file.exists():
                        pages.append(item.name)
        
        return {
            "success": True,
            "components": components,
            "pages": pages,
            "total_components": len(components),
            "total_pages": len(pages),
            "message": f"Se encontraron {len(components)} componentes y {len(pages)} páginas"
        }


# Instancia del agente
uiux_agent = UIUXAgent()
