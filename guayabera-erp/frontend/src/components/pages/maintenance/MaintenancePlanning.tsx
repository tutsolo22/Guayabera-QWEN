import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  ToolOutlined,
  CalendarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  UserOutlined,
  FileTextOutlined,
  CarOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const MaintenancePlanning: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('equipment');
  const [form] = Form.useForm();
  
  // Datos simulados para equipos
  const equipmentData = [
    { id: '1', nombre: 'Máquina de Coser Industrial', serie: 'MC-2023-001', ubicacion: 'Taller A', estado: 'activo', responsable: 'Carlos Gómez', ultima_revision: '2023-03-15' },
    { id: '2', nombre: 'Cortadora de Tela', serie: 'CT-2023-002', ubicacion: 'Corte', estado: 'activo', responsable: 'María López', ultima_revision: '2023-03-20' },
    { id: '3', nombre: 'Plancha de Vapor', serie: 'PV-2023-003', ubicacion: 'Acabados', estado: 'inactivo', responsable: 'Ana Martínez', ultima_revision: '2023-02-28' },
  ];

  // Datos simulados para órdenes de mantenimiento
  const orderData = [
    { id: '1', codigo: 'OM-2023-001', equipo: 'Máquina de Coser Industrial', tipo: 'preventivo', estado: 'programado', prioridad: 'media', responsable: 'Taller Mecánico SA', fecha_solicitud: '2023-04-01', fecha_programada: '2023-04-15' },
    { id: '2', codigo: 'OM-2023-002', equipo: 'Cortadora de Tela', tipo: 'correctivo', estado: 'en_progreso', prioridad: 'alta', responsable: 'Taller Mecánico SA', fecha_solicitud: '2023-04-10', fecha_programada: '2023-04-12' },
    { id: '3', codigo: 'OM-2023-003', equipo: 'Plancha de Vapor', tipo: 'preventivo', estado: 'completado', prioridad: 'baja', responsable: 'Taller Mecánico SA', fecha_solicitud: '2023-03-25', fecha_programada: '2023-04-01' },
  ];

  // Datos simulados para planes de mantenimiento
  const planData = [
    { id: '1', equipo: 'Máquina de Coser Industrial', descripcion: 'Mantenimiento mensual', frecuencia: 30, ultimo: '2023-03-15', proximo: '2023-04-15', activo: true },
    { id: '2', equipo: 'Cortadora de Tela', descripcion: 'Mantenimiento trimestral', frecuencia: 90, ultimo: '2023-03-20', proximo: '2023-06-20', activo: true },
    { id: '3', equipo: 'Plancha de Vapor', descripcion: 'Mantenimiento anual', frecuencia: 365, ultimo: '2022-12-15', proximo: '2023-12-15', activo: false },
  ];

  const columnasEquipos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Número de Serie', dataIndex: 'serie', key: 'serie' },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={estado === 'activo' ? 'green' : 'default'}>
          {estado}
        </Tag>
      )
    },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Última Revisión', dataIndex: 'ultima_revision', key: 'ultima_revision' },
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

  const columnasOrdenes = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Equipo', dataIndex: 'equipo', key: 'equipo' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'preventivo') color = 'blue';
        if (tipo === 'correctivo') color = 'orange';
        if (tipo === 'predictivo') color = 'green';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'programado') color = 'blue';
        if (estado === 'en_progreso') color = 'gold';
        if (estado === 'completado') color = 'green';
        if (estado === 'cancelado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { 
      title: 'Prioridad', 
      dataIndex: 'prioridad', 
      key: 'prioridad',
      render: (prioridad: string) => {
        let color = 'default';
        if (prioridad === 'baja') color = 'green';
        if (prioridad === 'media') color = 'blue';
        if (prioridad === 'alta') color = 'orange';
        if (prioridad === 'urgente') color = 'red';
        return <Tag color={color}>{prioridad}</Tag>;
      }
    },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Fecha Solicitud', dataIndex: 'fecha_solicitud', key: 'fecha_solicitud' },
    { title: 'Fecha Programada', dataIndex: 'fecha_programada', key: 'fecha_programada' },
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

  const columnasPlanes = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Equipo', dataIndex: 'equipo', key: 'equipo' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { title: 'Frecuencia (días)', dataIndex: 'frecuencia', key: 'frecuencia' },
    { title: 'Último Mantenimiento', dataIndex: 'ultimo', key: 'ultimo' },
    { title: 'Próximo Mantenimiento', dataIndex: 'proximo', key: 'proximo' },
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
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearEquipo = () => {
    setModalVisible(true);
  };

  const handleGuardarEquipo = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear equipo:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><ToolOutlined /> Planificación de Mantenimiento</Title>
          <Text>
            Programación preventiva de mantenimiento para activos y equipos
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearEquipo}>
            Nuevo {activeTab === 'equipment' ? 'Equipo' : 
                   activeTab === 'orders' ? 'Orden' : 
                   activeTab === 'plans' ? 'Plan' : 'Elemento'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Equipos Activos"
              value={124}
              prefix={<ToolOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Órdenes Abiertas"
              value={18}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Planes Activos"
              value={32}
              prefix={<CalendarOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Tareas Completadas"
              value={87}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="equipment" onChange={setActiveTab}>
        <TabPane tab="Equipos" key="equipment">
          <Card className="dashboard-card">
            <Table 
              dataSource={equipmentData} 
              columns={columnasEquipos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Órdenes de Mantenimiento" key="orders">
          <Card className="dashboard-card">
            <Table 
              dataSource={orderData} 
              columns={columnasOrdenes} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Planes de Mantenimiento" key="plans">
          <Card className="dashboard-card">
            <Table 
              dataSource={planData} 
              columns={columnasPlanes} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title={`Crear Nuevo ${activeTab === 'equipment' ? 'Equipo' : 
                 activeTab === 'orders' ? 'Orden de Mantenimiento' : 
                 activeTab === 'plans' ? 'Plan de Mantenimiento' : 'Elemento'}`}
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
          onFinish={handleGuardarEquipo}
        >
          {activeTab === 'equipment' && (
            <>
              <Form.Item name="nombre" label="Nombre del Equipo" rules={[{ required: true, message: 'Ingrese el nombre del equipo' }]}>
                <Input placeholder="Ej: Máquina de Coser Industrial" />
              </Form.Item>
              
              <Form.Item name="serie" label="Número de Serie" rules={[{ required: true, message: 'Ingrese el número de serie' }]}>
                <Input placeholder="Ej: MC-2023-001" />
              </Form.Item>
              
              <Form.Item name="descripcion" label="Descripción">
                <TextArea placeholder="Descripción del equipo y sus características" rows={4} />
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="ubicacion" label="Ubicación">
                    <Input placeholder="Ubicación física del equipo" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="estado" label="Estado" rules={[{ required: true, message: 'Seleccione el estado' }]}>
                    <Select placeholder="Seleccione el estado">
                      <Option value="activo">Activo</Option>
                      <Option value="inactivo">Inactivo</Option>
                      <Option value="fuera_servicio">Fuera de Servicio</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="responsable" label="Responsable del Equipo" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
                <Select placeholder="Seleccione el responsable">
                  <Option value="carlos_gomez">Carlos Gómez</Option>
                  <Option value="maria_lopez">María López</Option>
                  <Option value="ana_martinez">Ana Martínez</Option>
                  <Option value="luis_fernandez">Luis Fernández</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="fecha_adquisicion" label="Fecha de Adquisición">
                <Input type="date" />
              </Form.Item>
              
              <Form.Item name="proveedor" label="Proveedor">
                <Select placeholder="Seleccione el proveedor">
                  <Option value="maquinaria_industrial_sa">Maquinaria Industrial SA</Option>
                  <Option value="equipo_profesional_srl">Equipo Profesional SRL</Option>
                  <Option value="distribuciones_tecnologicas">Distribuciones Tecnológicas</Option>
                </Select>
              </Form.Item>
            </>
          )}
          
          {activeTab === 'orders' && (
            <>
              <Form.Item name="codigo" label="Código de la Orden" rules={[{ required: true, message: 'Ingrese el código de la orden' }]}>
                <Input placeholder="Ej: OM-2023-001" />
              </Form.Item>
              
              <Form.Item name="equipo" label="Equipo" rules={[{ required: true, message: 'Seleccione el equipo' }]}>
                <Select placeholder="Seleccione el equipo">
                  <Option value="maquina_coser">Máquina de Coser Industrial</Option>
                  <Option value="cortadora_tela">Cortadora de Tela</Option>
                  <Option value="plancha_vapor">Plancha de Vapor</Option>
                </Select>
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="tipo" label="Tipo de Mantenimiento" rules={[{ required: true, message: 'Seleccione el tipo' }]}>
                    <Select placeholder="Seleccione el tipo">
                      <Option value="preventivo">Preventivo</Option>
                      <Option value="correctivo">Correctivo</Option>
                      <Option value="predictivo">Predictivo</Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="prioridad" label="Prioridad" rules={[{ required: true, message: 'Seleccione la prioridad' }]}>
                    <Select placeholder="Seleccione la prioridad">
                      <Option value="baja">Baja</Option>
                      <Option value="media">Media</Option>
                      <Option value="alta">Alta</Option>
                      <Option value="urgente">Urgente</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="descripcion" label="Descripción del Trabajo">
                <TextArea placeholder="Descripción detallada del trabajo a realizar" rows={4} />
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="fecha_solicitud" label="Fecha de Solicitud" rules={[{ required: true, message: 'Seleccione la fecha de solicitud' }]}>
                    <Input type="date" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="fecha_programada" label="Fecha Programada" rules={[{ required: true, message: 'Seleccione la fecha programada' }]}>
                    <Input type="date" />
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="responsable" label="Responsable del Mantenimiento" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
                <Select placeholder="Seleccione el responsable">
                  <Option value="taller_mecanico_sa">Taller Mecánico SA</Option>
                  <Option value="mantenimiento_interno">Mantenimiento Interno</Option>
                  <Option value="tecnico_especializado">Técnico Especializado</Option>
                </Select>
              </Form.Item>
            </>
          )}
          
          {activeTab === 'plans' && (
            <>
              <Form.Item name="equipo" label="Equipo" rules={[{ required: true, message: 'Seleccione el equipo' }]}>
                <Select placeholder="Seleccione el equipo">
                  <Option value="maquina_coser">Máquina de Coser Industrial</Option>
                  <Option value="cortadora_tela">Cortadora de Tela</Option>
                  <Option value="plancha_vapor">Plancha de Vapor</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="descripcion" label="Descripción del Plan" rules={[{ required: true, message: 'Ingrese la descripción' }]}>
                <Input placeholder="Ej: Mantenimiento mensual preventivo" />
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="frecuencia" label="Frecuencia (días)" rules={[{ required: true, message: 'Ingrese la frecuencia en días' }]}>
                    <InputNumber 
                      placeholder="Días entre mantenimientos"
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="activo" label="Estado" rules={[{ required: true, message: 'Seleccione el estado' }]}>
                    <Select placeholder="Seleccione el estado">
                      <Option value={true}>Activo</Option>
                      <Option value={false}>Inactivo</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="ultimo_mantenimiento" label="Último Mantenimiento">
                    <Input type="date" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="proximo_mantenimiento" label="Próximo Mantenimiento" rules={[{ required: true, message: 'Seleccione la fecha del próximo mantenimiento' }]}>
                    <Input type="date" />
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="tareas" label="Tareas de Mantenimiento">
                <TextArea 
                  placeholder="Lista de tareas a realizar en cada mantenimiento" 
                  rows={4} 
                />
              </Form.Item>
            </>
          )}
          
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
                Crear {activeTab === 'equipment' ? 'Equipo' : 
                       activeTab === 'orders' ? 'Orden' : 
                       activeTab === 'plans' ? 'Plan' : 'Elemento'}
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default MaintenancePlanning;