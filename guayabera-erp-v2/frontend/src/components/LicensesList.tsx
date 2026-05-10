import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form as AntdForm, Input as AntdInput, Select as AntdSelect, DatePicker, message, Tag, Card, Space } from 'antd';
import moment from 'moment';
import axios from 'axios';

const { Option } = AntdSelect;
const { TextArea } = AntdInput;

const LicensesList: React.FC = () => {
  const [licenses, setLicenses] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingLicense, setEditingLicense] = useState<any>(null);
  const [form] = AntdForm.useForm();

  // Mock data for licenses
  useEffect(() => {
    // En una implementación real, esto llamaría a la API
    setLicenses([
      {
        id: '1',
        codigo: 'LIC-ABC-20260501',
        tenant_id: '1',
        tenant_name: 'Empresa ABC',
        tipo_licencia_id: '1',
        tipo_licencia_nombre: 'Prueba 90 días',
        fecha_inicio: '2026-05-01',
        fecha_fin: '2026-07-29',
        activa: true,
        usada: true,
        notas: 'Licencia de prueba inicial'
      },
      {
        id: '2',
        codigo: 'LIC-GT-20260415',
        tenant_id: '2',
        tenant_name: 'Grupo Tut',
        tipo_licencia_id: '2',
        tipo_licencia_nombre: 'Anual',
        fecha_inicio: '2026-04-15',
        fecha_fin: '2027-04-14',
        activa: true,
        usada: true,
        notas: 'Licencia anual adquirida'
      },
      {
        id: '3',
        codigo: 'LIC-AT-20260310',
        tenant_id: '3',
        tenant_name: 'Alexa Tut',
        tipo_licencia_id: '1',
        tipo_licencia_nombre: 'Prueba 90 días',
        fecha_inicio: '2026-03-10',
        fecha_fin: '2026-06-08',
        activa: true,
        usada: true,
        notas: 'Licencia de prueba para filial'
      },
      {
        id: '4',
        codigo: 'LIC-DEF-20260120',
        tenant_id: '4',
        tenant_name: 'Cliente DEF',
        tipo_licencia_id: '3',
        tipo_licencia_nombre: 'Mensual',
        fecha_inicio: '2026-01-20',
        fecha_fin: '2026-02-19',
        activa: false,
        usada: true,
        notas: 'Licencia mensual vencida'
      }
    ]);
  }, []);

  const showModal = (license?: any) => {
    if (license) {
      setEditingLicense(license);
      form.setFieldsValue({
        ...license,
        fecha_inicio: license.fecha_inicio ? moment(license.fecha_inicio) : null,
        fecha_fin: license.fecha_fin ? moment(license.fecha_fin) : null
      });
    } else {
      setEditingLicense(null);
      form.resetFields();
    }
    setModalVisible(true);
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingLicense) {
        // Update existing license
        console.log('Updating license:', values);
      } else {
        // Create new license
        console.log('Creating license:', values);
      }
      
      message.success(editingLicense ? 'Licencia actualizada exitosamente' : 'Licencia creada exitosamente');
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
    setEditingLicense(null);
    form.resetFields();
  };

  const columns = [
    {
      title: 'Código',
      dataIndex: 'codigo',
      key: 'codigo',
    },
    {
      title: 'Empresa',
      dataIndex: 'tenant_name',
      key: 'tenant_name',
    },
    {
      title: 'Tipo de Licencia',
      dataIndex: 'tipo_licencia_nombre',
      key: 'tipo_licencia_nombre',
    },
    {
      title: 'Fecha Inicio',
      dataIndex: 'fecha_inicio',
      key: 'fecha_inicio',
      render: (date: string) => moment(date).format('YYYY-MM-DD')
    },
    {
      title: 'Fecha Fin',
      dataIndex: 'fecha_fin',
      key: 'fecha_fin',
      render: (date: string) => moment(date).format('YYYY-MM-DD')
    },
    {
      title: 'Estado',
      key: 'estado',
      render: (record: any) => (
        <Space direction="vertical" size={0}>
          <Tag color={record.activa ? 'green' : 'red'}>
            {record.activa ? 'Activa' : 'Inactiva'}
          </Tag>
          <Tag color={record.usada ? 'blue' : 'orange'}>
            {record.usada ? 'Usada' : 'Sin usar'}
          </Tag>
        </Space>
      ),
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (record: any) => (
        <span>
          <Button type="link" onClick={() => showModal(record)}>Editar</Button>
          <Button danger type="link">Eliminar</Button>
        </span>
      ),
    },
  ];

  return (
    <Card title="Gestión de Licencias">
      <Button 
        type="primary" 
        style={{ marginBottom: 16 }} 
        onClick={() => showModal()}
      >
        Agregar Licencia
      </Button>
      
      <Table 
        dataSource={licenses} 
        columns={columns} 
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={editingLicense ? "Editar Licencia" : "Agregar Licencia"}
        visible={modalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Guardar"
        cancelText="Cancelar"
      >
        <AntdForm
          layout="vertical"
          form={form}
          name="license_form"
        >
          <AntdForm.Item
            name="codigo"
            label="Código de Licencia"
            rules={[{ required: true, message: 'Por favor ingrese el código de la licencia' }]}
          >
            <AntdInput id="codigo-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="tenant_id"
            label="Empresa (Tenant)"
            rules={[{ required: true, message: 'Por favor seleccione una empresa' }]}
          >
            <AntdSelect placeholder="Seleccione una empresa">
              <Option value="1">Empresa ABC</Option>
              <Option value="2">Grupo Tut</Option>
              <Option value="3">Alexa Tut</Option>
              <Option value="4">Cliente DEF</Option>
            </AntdSelect>
          </AntdForm.Item>
          
          <AntdForm.Item
            name="tipo_licencia_id"
            label="Tipo de Licencia"
            rules={[{ required: true, message: 'Por favor seleccione un tipo de licencia' }]}
          >
            <AntdSelect placeholder="Seleccione un tipo de licencia">
              <Option value="1">Prueba 90 días</Option>
              <Option value="2">Anual</Option>
              <Option value="3">Mensual</Option>
              <Option value="4">6 Meses</Option>
            </AntdSelect>
          </AntdForm.Item>
          
          <AntdForm.Item
            name="fecha_inicio"
            label="Fecha de Inicio"
          >
            <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="fecha_fin"
            label="Fecha de Finalización"
          >
            <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="activa"
            label="¿Está Activa?"
            rules={[{ required: true, message: 'Por favor seleccione si la licencia está activa' }]}
          >
            <AntdSelect 
              placeholder="Seleccione una opción" 
              options={[
                { value: 'true', label: 'Sí' },
                { value: 'false', label: 'No' }
              ]} 
            />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="notas"
            label="Notas"
          >
            <TextArea id="notas-textarea" rows={4} />
          </AntdForm.Item>
        </AntdForm>
      </Modal>
    </Card>
  );
};

export default LicensesList;