import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Progress, Timeline } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  ProjectOutlined,
  DollarOutlined,
  TeamOutlined,
  CalendarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  UserOutlined,
  FileTextOutlined,
  BarsOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { RangePicker } = DatePicker;

const ProjectManagementDashboard: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('projects');
  const [form] = Form.useForm();
  
  // Datos simulados para proyectos
  const projectData = [
    { id: '1', nombre: 'Lanzamiento Colección Otoño', cliente: 'Moda S.A.', estado: 'en_progreso', inicio: '2023-03-01', fin: '2023-06-30', costo: 250000, avance: 65, gerente: 'Ana López' },
    { id: '2', nombre: 'Optimización Cadena Suministro', cliente: 'Internacional S.A.', estado: 'planeado', inicio: '2023-05-15', fin: '2023-08-30', costo: 180000, avance: 0, gerente: 'Carlos Gómez' },
    { id: '3', nombre: 'Implementación Nuevos Equipos', cliente: 'Tecnología SA', estado: 'completado', inicio: '2023-01-10', fin: '2023-04-20', costo: 420000, avance: 100, gerente: 'María Rodríguez' },
  ];

  // Datos simulados para tareas
  const taskData = [
    { id: '1', proyecto: 'Lanzamiento Colección Otoño', titulo: 'Diseño de prendas', responsable: 'Diseñador 1', estado: 'completado', inicio: '2023-03-01', fin: '2023-03-15', duracion: 15 },
    { id: '2', proyecto: 'Lanzamiento Colección Otoño', titulo: 'Selección de telas', responsable: 'Comprador 1', estado: 'en_progreso', inicio: '2023-03-10', fin: '2023-03-25', duracion: 15 },
    { id: '3', proyecto: 'Lanzamiento Colección Otoño', titulo: 'Producción de prototipos', responsable: 'Jefe Producción', estado: 'pendiente', inicio: '2023-03-20', fin: '2023-04-10', duracion: 21 },
    { id: '4', proyecto: 'Optimización Cadena Suministro', titulo: 'Análisis logístico actual', responsable: 'Consultor 1', estado: 'pendiente', inicio: '2023-05-15', fin: '2023-06-05', duracion: 21 },
  ];

  // Datos simulados para costos
  const costData = [
    { id: '1', proyecto: 'Lanzamiento Colección Otoño', concepto: 'Materiales', monto: 85000, fecha: '2023-03-10', estado_pago: 'pagado' },
    { id: '2', proyecto: 'Lanzamiento Colección Otoño', concepto: 'Mano de obra', monto: 45000, fecha: '2023-03-20', estado_pago: 'pendiente' },
    { id: '3', proyecto: 'Lanzamiento Colección Otoño', concepto: 'Diseño', monto: 32000, fecha: '2023-03-05', estado_pago: 'pagado' },
    { id: '4', proyecto: 'Implementación Nuevos Equipos', concepto: 'Equipos', monto: 320000, fecha: '2023-02-15', estado_pago: 'pagado' },
  ];

  const columnasProyectos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'planeado') color = 'blue';
        if (estado === 'en_progreso') color = 'orange';
        if (estado === 'completado') color = 'green';
        if (estado === 'cancelado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Inicio', dataIndex: 'inicio', key: 'inicio' },
    { title: 'Fin', dataIndex: 'fin', key: 'fin' },
    { 
      title: 'Costo', 
      dataIndex: 'costo', 
      key: 'costo',
      render: (costo: number) => `$${costo.toLocaleString()}`
    },
    { 
      title: 'Avance', 
      dataIndex: 'avance', 
      key: 'avance',
      render: (avance: number) => (
        <div>
          <Progress percent={avance} size="small" />
          <Text>{avance}%</Text>
        </div>
      )
    },
    { title: 'Gerente', dataIndex: 'gerente', key: 'gerente' },
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

  const columnasTareas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Proyecto', dataIndex: 'proyecto', key: 'proyecto' },
    { title: 'Tarea', dataIndex: 'titulo', key: 'titulo' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'en_progreso') color = 'blue';
        if (estado === 'completado') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Inicio', dataIndex: 'inicio', key: 'inicio' },
    { title: 'Fin', dataIndex: 'fin', key: 'fin' },
    { 
      title: 'Duración (días)', 
      dataIndex: 'duracion', 
      key: 'duracion'
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

  const columnasCostos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Proyecto', dataIndex: 'proyecto', key: 'proyecto' },
    { title: 'Concepto', dataIndex: 'concepto', key: 'concepto' },
    { 
      title: 'Monto', 
      dataIndex: 'monto', 
      key: 'monto',
      render: (monto: number) => `$${monto.toLocaleString()}`
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { 
      title: 'Estado de Pago', 
      dataIndex: 'estado_pago', 
      key: 'estado_pago',
      render: (estado_pago: string) => {
        let color = 'default';
        if (estado_pago === 'pagado') color = 'green';
        if (estado_pago === 'pendiente') color = 'orange';
        if (estado_pago === 'vencido') color = 'red';
        return <Tag color={color}>{estado_pago}</Tag>;
      }
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

  const handleCrearProyecto = () => {
    setModalVisible(true);
  };

  const handleGuardarProyecto = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear proyecto:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><ProjectOutlined /> Gestión de Proyectos</Title>
          <Text>
            Seguimiento de costos, tiempos y recursos por proyecto, facturación por etapas y matrices de responsabilidades
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearProyecto}>
            Nuevo {activeTab === 'projects' ? 'Proyecto' : 
                   activeTab === 'tasks' ? 'Tarea' : 
                   activeTab === 'costs' ? 'Costo' : 'Proyecto'}
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="projects" onChange={setActiveTab}>
        <TabPane tab="Proyectos" key="projects">
          <Card className="dashboard-card">
            <Table 
              dataSource={projectData} 
              columns={columnasProyectos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Tareas" key="tasks">
          <Card className="dashboard-card">
            <Table 
              dataSource={taskData} 
              columns={columnasTareas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Costos" key="costs">
          <Card className="dashboard-card">
            <Table 
              dataSource={costData} 
              columns={columnasCostos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title={`Crear Nuevo ${activeTab === 'projects' ? 'Proyecto' : 
                 activeTab === 'tasks' ? 'Tarea' : 
                 activeTab === 'costs' ? 'Costo' : 'Proyecto'}`}
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
          onFinish={handleGuardarProyecto}
        >
          {activeTab === 'projects' && (
            <>
              <Form.Item name="nombre" label="Nombre del Proyecto" rules={[{ required: true, message: 'Ingrese el nombre del proyecto' }]}>
                <Input placeholder="Ej: Lanzamiento de Nueva Colección" />
              </Form.Item>
              
              <Form.Item name="cliente" label="Cliente" rules={[{ required: true, message: 'Seleccione el cliente' }]}>
                <Select placeholder="Seleccione el cliente">
                  <Option value="moda_sa">Moda S.A.</Option>
                  <Option value="internacional_sa">Internacional S.A.</Option>
                  <Option value="tecnologia_sa">Tecnología SA</Option>
                  <Option value="textil_mundo">Textil Mundo SRL</Option>
                </Select>
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="inicio" label="Fecha de Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="fin" label="Fecha de Finalización" rules={[{ required: true, message: 'Seleccione la fecha de finalización' }]}>
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="costo" label="Costo Estimado" rules={[{ required: true, message: 'Ingrese el costo estimado' }]}>
                    <InputNumber 
                      placeholder="Costo estimado del proyecto"
                      style={{ width: '100%' }}
                      formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                      parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="gerente" label="Gerente del Proyecto" rules={[{ required: true, message: 'Seleccione el gerente del proyecto' }]}>
                    <Select placeholder="Seleccione el gerente">
                      <Option value="ana_lopez">Ana López</Option>
                      <Option value="carlos_gomez">Carlos Gómez</Option>
                      <Option value="maria_rodriguez">María Rodríguez</Option>
                      <Option value="jose_fernandez">José Fernández</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="estado" label="Estado del Proyecto" rules={[{ required: true, message: 'Seleccione el estado del proyecto' }]}>
                <Select placeholder="Seleccione el estado">
                  <Option value="planeado">Planeado</Option>
                  <Option value="en_progreso">En Progreso</Option>
                  <Option value="completado">Completado</Option>
                  <Option value="cancelado">Cancelado</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="descripcion" label="Descripción">
                <TextArea placeholder="Descripción detallada del proyecto" rows={4} />
              </Form.Item>
            </>
          )}
          
          {activeTab === 'tasks' && (
            <>
              <Form.Item name="proyecto" label="Proyecto Asociado" rules={[{ required: true, message: 'Seleccione el proyecto' }]}>
                <Select placeholder="Seleccione el proyecto">
                  <Option value="lanzamiento_otono">Lanzamiento Colección Otoño</Option>
                  <Option value="optimizacion_cadena">Optimización Cadena Suministro</Option>
                  <Option value="implementacion_equipos">Implementación Nuevos Equipos</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="titulo" label="Título de la Tarea" rules={[{ required: true, message: 'Ingrese el título de la tarea' }]}>
                <Input placeholder="Ej: Diseño de prendas" />
              </Form.Item>
              
              <Form.Item name="descripcion" label="Descripción">
                <TextArea placeholder="Descripción detallada de la tarea" rows={4} />
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="responsable" label="Responsable" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
                    <Select placeholder="Seleccione el responsable">
                      <Option value="disenador_1">Diseñador 1</Option>
                      <Option value="comprador_1">Comprador 1</Option>
                      <Option value="jefe_produccion">Jefe de Producción</Option>
                      <Option value="consultor_1">Consultor 1</Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="estado" label="Estado" rules={[{ required: true, message: 'Seleccione el estado' }]}>
                    <Select placeholder="Seleccione el estado">
                      <Option value="pendiente">Pendiente</Option>
                      <Option value="en_progreso">En Progreso</Option>
                      <Option value="completado">Completado</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="inicio" label="Fecha de Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="fin" label="Fecha de Finalización" rules={[{ required: true, message: 'Seleccione la fecha de finalización' }]}>
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>
            </>
          )}
          
          {activeTab === 'costs' && (
            <>
              <Form.Item name="proyecto" label="Proyecto Asociado" rules={[{ required: true, message: 'Seleccione el proyecto' }]}>
                <Select placeholder="Seleccione el proyecto">
                  <Option value="lanzamiento_otono">Lanzamiento Colección Otoño</Option>
                  <Option value="optimizacion_cadena">Optimización Cadena Suministro</Option>
                  <Option value="implementacion_equipos">Implementación Nuevos Equipos</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="concepto" label="Concepto del Gasto" rules={[{ required: true, message: 'Ingrese el concepto del gasto' }]}>
                <Input placeholder="Ej: Materiales, Mano de obra, etc." />
              </Form.Item>
              
              <Form.Item name="monto" label="Monto" rules={[{ required: true, message: 'Ingrese el monto' }]}>
                <InputNumber 
                  placeholder="Monto del gasto"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
              
              <Form.Item name="fecha" label="Fecha del Gasto" rules={[{ required: true, message: 'Seleccione la fecha del gasto' }]}>
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
              
              <Form.Item name="estado_pago" label="Estado de Pago" rules={[{ required: true, message: 'Seleccione el estado de pago' }]}>
                <Select placeholder="Seleccione el estado de pago">
                  <Option value="pagado">Pagado</Option>
                  <Option value="pendiente">Pendiente</Option>
                  <Option value="vencido">Vencido</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="descripcion" label="Descripción">
                <TextArea placeholder="Descripción detallada del gasto" rows={4} />
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
                Crear {activeTab === 'projects' ? 'Proyecto' : 
                       activeTab === 'tasks' ? 'Tarea' : 
                       activeTab === 'costs' ? 'Costo' : 'Elemento'}
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ProjectManagementDashboard;