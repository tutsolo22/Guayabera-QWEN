import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Card, Tag, Space } from 'antd';
import axios from 'axios';

const { TextArea } = Input;

const TenantsList: React.FC = () => {
  const [tenants, setTenants] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTenant, setEditingTenant] = useState<any>(null);

  // Mock data for tenants
  useEffect(() => {
    // En una implementación real, esto llamaría a la API
    setTenants([
      {
        id: '1',
        name: 'Empresa ABC',
        subdomain: 'abc',
        schema_name: 'tenant_abc',
        is_active: true,
        contact_email: 'contacto@empresaabc.com',
        contact_phone: '+52 123 456 7890',
        descripcion: 'Empresa dedicada a la producción textil',
        es_grupo_corporativo: false,
        grupo_corporativo_id: null
      },
      {
        id: '2',
        name: 'Grupo Tut',
        subdomain: 'grupotut',
        schema_name: 'tenant_grupotut',
        is_active: true,
        contact_email: 'info@grupotut.com',
        contact_phone: '+52 987 654 3210',
        descripcion: 'Grupo corporativo con varias filiales',
        es_grupo_corporativo: true,
        grupo_corporativo_id: null
      },
      {
        id: '3',
        name: 'Alexa Tut',
        subdomain: 'alexatut',
        schema_name: 'tenant_alexatut',
        is_active: true,
        contact_email: 'alexa@tut.com',
        contact_phone: '+52 111 222 3333',
        descripcion: 'Filia de Grupo Tut',
        es_grupo_corporativo: false,
        grupo_corporativo_id: '2'
      }
    ]);
  }, []);

  const showModal = (tenant?: any) => {
    if (tenant) {
      setEditingTenant(tenant);
      form.setFieldsValue(tenant);
    } else {
      setEditingTenant(null);
      form.resetFields();
    }
    setModalVisible(true);
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingTenant) {
        // Update existing tenant
        console.log('Updating tenant:', values);
      } else {
        // Create new tenant
        console.log('Creating tenant:', values);
      }
      
      message.success(editingTenant ? 'Tenant actualizado exitosamente' : 'Tenant creado exitosamente');
      setModalVisible(false);
      form.resetFields();
      
      // Refresh the list
      // In a real implementation, this would call the API
    } catch (error) {
      console.log('Validation failed:', error);
    }
  };

  const handleCancel = () => {
    setModalVisible(false);
    setEditingTenant(null);
    form.resetFields();
  };

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Subdominio',
      dataIndex: 'subdomain',
      key: 'subdomain',
    },
    {
      title: 'Email de Contacto',
      dataIndex: 'contact_email',
      key: 'contact_email',
    },
    {
      title: 'Teléfono',
      dataIndex: 'contact_phone',
      key: 'contact_phone',
    },
    {
      title: 'Es Grupo Corporativo',
      key: 'es_grupo_corporativo',
      render: (record: any) => (
        <Tag color={record.es_grupo_corporativo ? 'blue' : 'default'}>{record.es_grupo_corporativo ? 'Sí' : 'No'}</Tag>
      ),
    },
    {
      title: 'Estado',
      key: 'is_active',
      render: (record: any) => (
        <Tag color={record.is_active ? 'green' : 'red'}>{record.is_active ? 'Activo' : 'Inactivo'}</Tag>
      ),
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (record: any) => (
      <Space>
        <Button type="link" onClick={() => showModal(record)}>Editar</Button>
        <Button danger type="link">Eliminar</Button>
      </Space>
      ),
    },
  ];

  return (
    <Card title="Gestión de Empresas (Tenants)">
      <Button 
        type="primary" 
        style={{ marginBottom: 16 }} 
        onClick={() => showModal()}
      >
        Agregar Empresa
      </Button>
      
      <Table 
        dataSource={tenants} 
        columns={columns} 
        loading={loading}
        rowKey="id"
      />
      
      <Modal
        title={editingTenant ? "Editar Empresa" : "Agregar Empresa"}
        open={modalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Guardar"
        cancelText="Cancelar"
      >
        {/* @ts-ignore */}
        <Form
          layout="vertical"
          name="tenant_form"
        >
          <Form.Item
            name="name"
            label="Nombre de la Empresa"
            rules={[{ required: true, message: 'Por favor ingrese el nombre de la empresa' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="subdomain"
            label="Subdominio"
            rules={[{ required: true, message: 'Por favor ingrese el subdominio' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="contact_email"
            label="Email de Contacto"
            rules={[{ type: 'email', message: 'Ingrese un email válido' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="contact_phone"
            label="Teléfono de Contacto"
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="descripcion"
            label="Descripción"
          >
            <TextArea rows={4} />
          </Form.Item>
          
          <Form.Item
            name="es_grupo_corporativo"
            label="¿Es Grupo Corporativo?"
            rules={[{ required: true, message: 'Por favor seleccione una opción' }]}
          >
            <Select placeholder="Seleccione una opción">
              <Select.Option value="true">Sí</Select.Option>
              <Select.Option value="false">No</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default TenantsList;