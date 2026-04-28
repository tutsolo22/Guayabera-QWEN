import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Switch, Steps } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  SettingOutlined,
  GatewayOutlined,
  StepForwardOutlined,
  BranchesOutlined,
  UserSwitchOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { Step } = Steps;

const WorkflowManagement: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [stepModalVisible, setStepModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('workflows');
  const [form] = Form.useForm();
  const [stepForm] = Form.useForm();
  
  // Datos simulados para flujos de trabajo
  const workflowData = [
    { id: '1', nombre: 'Aprobación de Cotización', descripcion: 'Flujo para aprobar cotizaciones superiores a $50,000', activo: true, pasos: 4, modulo: 'ventas' },
    { id: '2', nombre: 'Recepción de Mercancía', descripcion: 'Flujo para recibir mercancía en almacén', activo: true, pasos: 3, modulo: 'inventario' },
    { id: '3', nombre: 'Solicitud de Compra', descripcion: 'Flujo para solicitudes de compra de insumos', activo: false, pasos: 5, modulo: 'compras' },
    { id: '4', nombre: 'Incidencia de Personal', descripcion: 'Flujo para reportar incidencias de personal', activo: true, pasos: 3, modulo: 'rh' },
  ];

  // Datos simulados para pasos de flujo
  const stepData = [
    { id: '1', flujo: 'Aprobación de Cotización', nombre: 'Validación Inicial', responsable: 'Vendedor', tipo: 'validacion', orden: 1 },
    { id: '2', flujo: 'Aprobación de Cotización', nombre: 'Revisión Gerente', responsable: 'Gerente Ventas', tipo: 'aprobacion', orden: 2 },
    { id: '3', flujo: 'Aprobación de Cotización', nombre: 'Revisión Finanzas', responsable: 'Jefe Finanzas', tipo: 'aprobacion', orden: 3 },
    { id: '4', flujo: 'Aprobación de Cotización', nombre: 'Aprobación Final', responsable: 'Director', tipo: 'aprobacion', orden: 4 },
  ];

  const columnasFlujos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { title: 'Módulo', dataIndex: 'modulo', key: 'modulo' },
    { title: 'Pasos', dataIndex: 'pasos', key: 'pasos' },
    { 
      title: 'Estado', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        <Tag color={activo ? 'green' : 'default'}>
          {activo ? 'Activo' : 'Inactivo'}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<BranchesOutlined />} onClick={() => setStepModalVisible(true)}>Ver Pasos</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasPasos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Flujo', dataIndex: 'flujo', key: 'flujo' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'validacion') color = 'blue';
        if (tipo === 'aprobacion') color = 'green';
        if (tipo === 'notificacion') color = 'orange';
        if (tipo === 'rechazo') color = 'red';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Orden', dataIndex: 'orden', key: 'orden' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearFlujo = () => {
    setModalVisible(true);
  };

  const handleCrearPaso = () => {
    setStepModalVisible(true);
  };

  const handleGuardarFlujo = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear flujo:', error);
    }
  };

  const handleGuardarPaso = async () => {
    try {
      const values = await stepForm.validateFields();
      console.log('Valores del formulario:', values);
      setStepModalVisible(false);
      stepForm.resetFields();
    } catch (error) {
      console.error('Error al crear paso:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><GatewayOutlined /> Flujos de Trabajo Personalizados</Title>
          <Text>
            Configuración de procesos automatizados y flujos de trabajo según las necesidades del negocio
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'workflows' ? handleCrearFlujo : handleCrearPaso}>
            Nuevo {activeTab === 'workflows' ? 'Flujo' : 'Paso'}
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="workflows" onChange={setActiveTab}>
        <TabPane tab="Flujos de Trabajo" key="workflows">
          <Card className="dashboard-card">
            <Table 
              dataSource={workflowData} 
              columns={columnasFlujos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Pasos de Flujo" key="steps">
          <Card className="dashboard-card">
            <Table 
              dataSource={stepData} 
              columns={columnasPasos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Flujo de Trabajo"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarFlujo}
        >
          <Form.Item name="nombre" label="Nombre del Flujo" rules={[{ required: true, message: 'Ingrese el nombre del flujo' }]}>
            <Input placeholder="Ej: Aprobación de Cotización" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción detallada del flujo de trabajo" rows={4} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="modulo" label="Módulo Asociado" rules={[{ required: true, message: 'Seleccione el módulo asociado' }]}>
                <Select placeholder="Seleccione el módulo">
                  <Option value="ventas">Ventas</Option>
                  <Option value="inventario">Inventario</Option>
                  <Option value="compras">Compras</Option>
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="produccion">Producción</Option>
                  <Option value="contabilidad">Contabilidad</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="activo" label="Estado" valuePropName="checked">
                <Switch checkedChildren="Activo" unCheckedChildren="Inactivo" defaultChecked />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="condiciones_inicio" label="Condiciones de Inicio">
            <TextArea placeholder="Condiciones que deben cumplirse para iniciar este flujo" rows={3} />
          </Form.Item>
          
          <Form.Item name="notificaciones" label="Notificaciones">
            <Select 
              mode="multiple" 
              placeholder="Seleccione los tipos de notificaciones"
              allowClear
            >
              <Option value="email">Correo Electrónico</Option>
              <Option value="sms">SMS</Option>
              <Option value="sistema">Notificación Interna</Option>
              <Option value="push">Notificación Push</Option>
            </Select>
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
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Flujo
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Crear Nuevo Paso de Flujo"
        open={stepModalVisible}
        onCancel={() => {
          setStepModalVisible(false);
          stepForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={stepForm}
          layout="vertical"
          onFinish={handleGuardarPaso}
        >
          <Form.Item name="flujo" label="Flujo Asociado" rules={[{ required: true, message: 'Seleccione el flujo asociado' }]}>
            <Select placeholder="Seleccione el flujo">
              <Option value="aprobacion_cotizacion">Aprobación de Cotización</Option>
              <Option value="recepcion_mercancia">Recepción de Mercancía</Option>
              <Option value="solicitud_compra">Solicitud de Compra</Option>
              <Option value="incidencia_personal">Incidencia de Personal</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="nombre" label="Nombre del Paso" rules={[{ required: true, message: 'Ingrese el nombre del paso' }]}>
            <Input placeholder="Ej: Validación Inicial" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción detallada del paso" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Paso" rules={[{ required: true, message: 'Seleccione el tipo de paso' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="validacion">Validación</Option>
                  <Option value="aprobacion">Aprobación</Option>
                  <Option value="notificacion">Notificación</Option>
                  <Option value="rechazo">Rechazo</Option>
                  <Option value="automatizado">Automatizado</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="orden" label="Orden del Paso" rules={[{ required: true, message: 'Ingrese el orden del paso' }]}>
                <InputNumber 
                  placeholder="Número de orden"
                  min={1}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="responsable" label="Responsable del Paso" rules={[{ required: true, message: 'Seleccione el responsable del paso' }]}>
            <Select placeholder="Seleccione el responsable">
              <Option value="vendedor">Vendedor</Option>
              <Option value="gerente_ventas">Gerente de Ventas</Option>
              <Option value="jefe_finanzas">Jefe de Finanzas</Option>
              <Option value="director">Director</Option>
              <Option value="almacenero">Almacenero</Option>
              <Option value="jefe_produccion">Jefe de Producción</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="condiciones" label="Condiciones para Ejecución">
            <TextArea placeholder="Condiciones que deben cumplirse para ejecutar este paso" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setStepModalVisible(false);
                stepForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Paso
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default WorkflowManagement;