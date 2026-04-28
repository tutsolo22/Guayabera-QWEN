import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, DatePicker, InputNumber, Tabs, Divider, message } from 'antd';
import { 
  UserAddOutlined, 
  TeamOutlined, 
  CalendarOutlined, 
  FileTextOutlined, 
  ClockCircleOutlined,
  MedicineBoxOutlined,
  BellOutlined,
  LaptopOutlined
} from '@ant-design/icons';
import HRDashboardNewFeatures from './HRDashboardNewFeatures';

const { Title } = Typography;

const HRDashboard: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para empleados
  const empleadosData = [
    { key: '1', id: 'EMP-001', nombre: 'Juan Pérez', puesto: 'Desarrollador', departamento: 'TI', estado: 'activo' },
    { key: '2', id: 'EMP-002', nombre: 'María López', puesto: 'Contadora', departamento: 'Finanzas', estado: 'activo' },
    { key: '3', id: 'EMP-003', nombre: 'Carlos Ramírez', puesto: 'Supervisor', departamento: 'Producción', estado: 'inactivo' },
  ];

  const columnasEmpleados = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Puesto', dataIndex: 'puesto', key: 'puesto' },
    { title: 'Departamento', dataIndex: 'departamento', key: 'departamento' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={estado === 'activo' ? 'green' : 'red'}>
          {estado}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
          <Button type="link">Editar</Button>
        </Space>
      ),
    },
  ];

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      message.success('Empleado creado exitosamente');
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear empleado:', error);
      message.error('Error al crear el empleado');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Recursos Humanos</Title>
          <Typography.Text>
            Gestión de empleados, nóminas, asistencias y beneficios
          </Typography.Text>
        </div>
        <Space>
          <Button type="primary" icon={<UserAddOutlined />} onClick={() => setModalVisible(true)}>
            Nuevo Empleado
          </Button>
          <Button icon={<BellOutlined />} onClick={() => window.location.hash = "/hr/anuncios-vacaciones"}>
            Anuncios y Vacaciones
          </Button>
        </Space>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Empleados" 
              value={124} 
              prefix={<TeamOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Departamentos" 
              value={12} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Vacaciones" 
              value={8} 
              prefix={<CalendarOutlined />} 
              valueStyle={{ color: '#cf1322' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Incapacidades" 
              value={4} 
              prefix={<MedicineBoxOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Tabs 
          defaultActiveKey="1" 
          items={[
            {
              label: 'Empleados',
              key: '1',
              children: (
                <Table 
                  dataSource={empleadosData} 
                  columns={columnasEmpleados} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Asistencias',
              key: '2',
              children: <p>Asistencias de empleados</p>,
            },
            {
              label: 'Nóminas',
              key: '3',
              children: <p>Nóminas de empleados</p>,
            },
          ]} 
        />
      </Card>

      <Modal
        title="Crear Nuevo Empleado"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="nombre" label="Nombre Completo" rules={[{ required: true, message: 'Ingrese el nombre del empleado' }]}>
                <Input placeholder="Nombre completo del empleado" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="puesto" label="Puesto" rules={[{ required: true, message: 'Ingrese el puesto del empleado' }]}>
                <Input placeholder="Puesto del empleado" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="departamento" label="Departamento" rules={[{ required: true, message: 'Seleccione el departamento' }]}>
                <Select placeholder="Seleccione el departamento">
                  <Option value="ti">TI</Option>
                  <Option value="finanzas">Finanzas</Option>
                  <Option value="ventas">Ventas</Option>
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="produccion">Producción</Option>
                  <Option value="logistica">Logística</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="correo" label="Correo Electrónico" rules={[
                { type: 'email', message: 'Ingrese un correo electrónico válido' },
                { required: true, message: 'Ingrese el correo electrónico' }
              ]}>
                <Input placeholder="correo@empresa.com" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="telefono" label="Teléfono">
                <Input placeholder="Teléfono del empleado" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fechaContratacion" label="Fecha de Contratación">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="direccion" label="Dirección">
            <Input.TextArea placeholder="Dirección del empleado" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<UserAddOutlined />}>
                Crear Empleado
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default HRDashboard;