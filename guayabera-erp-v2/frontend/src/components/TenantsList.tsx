import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form as AntdForm, Input as AntdInput, Select as AntdSelect, message, Tag, Space } from 'antd';
import axios from 'axios';

const TenantsList: React.FC = () => {
  const [tenants, setTenants] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTenant, setEditingTenant] = useState<any>(null);
  const [form] = AntdForm.useForm();

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

  // Filter non-corporate tenants to use as subsidiaries
  const nonCorporateTenants = tenants.filter(tenant => !tenant.es_grupo_corporativo);
  
  // Filter corporate group tenants to assign as parent
  const corporateTenants = tenants.filter(tenant => tenant.es_grupo_corporativo);

  return (
    <div style={{ padding: 24 }}>
      <h2 style={{ color: '#1B365D', marginBottom: 16 }}>Gestión de Empresas (Tenants)</h2>
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
        <AntdForm
          layout="vertical"
          form={form}
          name="tenant_form"
        >
          <AntdForm.Item
            name="name"
            label="Nombre de la Empresa"
            rules={[{ required: true, message: 'Por favor ingrese el nombre de la empresa' }]}
          >
            <AntdInput id="name-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="subdomain"
            label="Subdominio"
            rules={[{ required: true, message: 'Por favor ingrese el subdominio' }]}
          >
            <AntdInput id="subdomain-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="contact_email"
            label="Email de Contacto"
            rules={[{ type: 'email', message: 'Ingrese un email válido' }]}
          >
            <AntdInput id="email-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="contact_phone"
            label="Teléfono de Contacto"
          >
            <AntdInput id="phone-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="descripcion"
            label="Descripción"
          >
            <AntdInput.TextArea id="description-input" rows={4} />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="es_grupo_corporativo"
            label="¿Es Grupo Corporativo?"
            valuePropName="checked"
          >
            <AntdSelect id="corporate-group-select" placeholder="Seleccione una opción">
              <AntdSelect.Option value="true">Sí</AntdSelect.Option>
              <AntdSelect.Option value="false">No</AntdSelect.Option>
            </AntdSelect>
          </AntdForm.Item>
          
          {/* Conditional field to select parent corporate group if this is a subsidiary */}
          <AntdForm.Item 
            noStyle
            shouldUpdate={(prevValues, currentValues) => prevValues.es_grupo_corporativo !== currentValues.es_grupo_corporativo}
          >
            {({ getFieldValue }) => {
              const isCorporateGroup = getFieldValue('es_grupo_corporativo') === 'false';
              
              if (!isCorporateGroup) {
                return (
                  <AntdForm.Item
                    name="grupo_corporativo_id"
                    label="Grupo Corporativo al que Pertenece"
                  >
                    <AntdSelect id="parent-corp-select" placeholder="Seleccione el grupo corporativo">
                      {/* This would be populated with actual corporate groups */}
                      <AntdSelect.Option value="2">Grupo Corporativo XYZ</AntdSelect.Option>
                    </AntdSelect>
                  </AntdForm.Item>
                );
              }
              return null;
            }}
          </AntdForm.Item>
        </AntdForm>
      </Modal>
      </div>
  );
};

export default TenantsList;