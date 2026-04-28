import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, Switch, Tabs, Divider, message, Alert } from 'antd';
import { 
  ToolOutlined, 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  DeploymentUnitOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ThunderboltOutlined,
  ApiOutlined,
  EyeOutlined,
  DownloadOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

interface CADAgent {
  key: string;
  id: string;
  nombre: string;
  estado: 'activo' | 'inactivo' | 'ocupado';
  tipo: 'dibujo' | 'render' | 'simulacion';
  capacidad: string;
  ubicacion: string;
  ultimaConexion: string;
  version: string;
}

interface CADTask {
  key: string;
  id: string;
  nombreTarea: string;
  agente: string;
  estado: 'pendiente' | 'procesando' | 'completado' | 'fallido';
  fechaCreacion: string;
  progreso: number;
  tipo: string;
}

const CADAgents: React.FC = () => {
  const [agentModalVisible, setAgentModalVisible] = useState(false);
  const [tasksModalVisible, setTasksModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para agentes CAD
  const agentsData: CADAgent[] = [
    { key: '1', id: 'CA-001', nombre: 'Agente Renderizado Principal', estado: 'ocupado', tipo: 'render', capacidad: '8 núcleos, 16GB RAM', ubicacion: 'Servidor Local', ultimaConexion: '2023-04-18 10:30', version: '2.1.4' },
    { key: '2', id: 'CA-002', nombre: 'Agente Dibujo Remoto', estado: 'activo', tipo: 'dibujo', capacidad: '4 núcleos, 8GB RAM', ubicacion: 'Estación de Diseño 1', ultimaConexion: '2023-04-18 09:45', version: '2.1.3' },
    { key: '3', id: 'CA-003', nombre: 'Agente Simulación', estado: 'activo', tipo: 'simulacion', capacidad: '16 núcleos, 32GB RAM', ubicacion: 'Laboratorio de Pruebas', ultimaConexion: '2023-04-18 10:15', version: '2.2.1' },
    { key: '4', id: 'CA-004', nombre: 'Agente Dibujo Auxiliar', estado: 'inactivo', tipo: 'dibujo', capacidad: '4 núcleos, 8GB RAM', ubicacion: 'Estación de Diseño 2', ultimaConexion: '2023-04-17 16:20', version: '2.0.9' },
  ];

  // Datos simulados para tareas CAD
  const tasksData: CADTask[] = [
    { key: '1', id: 'CT-001', nombreTarea: 'Renderizado Modelo 3D', agente: 'Agente Renderizado Principal', estado: 'procesando', fechaCreacion: '2023-04-18 09:30', progreso: 65, tipo: 'render' },
    { key: '2', id: 'CT-002', nombreTarea: 'Diseño Nuevo Producto', agente: 'Agente Dibujo Remoto', estado: 'completado', fechaCreacion: '2023-04-18 08:15', progreso: 100, tipo: 'dibujo' },
    { key: '3', id: 'CT-003', nombreTarea: 'Simulación Resistencia', agente: 'Agente Simulación', estado: 'pendiente', fechaCreacion: '2023-04-18 10:45', progreso: 0, tipo: 'simulacion' },
    { key: '4', id: 'CT-004', nombreTarea: 'Optimización Geometría', agente: 'Agente Dibujo Remoto', estado: 'completado', fechaCreacion: '2023-04-18 07:20', progreso: 100, tipo: 'dibujo' },
  ];

  const columnasAgentes = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        let text = estado;
        if (estado === 'activo') color = 'green';
        if (estado === 'inactivo') color = 'default';
        if (estado === 'ocupado') color = 'orange';
        return <Tag color={color}>{text}</Tag>;
      }
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'dibujo') color = 'blue';
        if (tipo === 'render') color = 'geekblue';
        if (tipo === 'simulacion') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Capacidad', dataIndex: 'capacidad', key: 'capacidad' },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { title: 'Última Conexión', dataIndex: 'ultimaConexion', key: 'ultimaConexion' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EyeOutlined />}>Estado</Button>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
          <Button type="link" icon={<ThunderboltOutlined />}>Reiniciar</Button>
        </Space>
      ),
    },
  ];

  const columnasTareas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Tarea', dataIndex: 'nombreTarea', key: 'nombreTarea' },
    { title: 'Agente', dataIndex: 'agente', key: 'agente' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        let text = estado;
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'procesando') color = 'blue';
        if (estado === 'completado') color = 'green';
        if (estado === 'fallido') color = 'red';
        return <Tag color={color}>{text}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fechaCreacion', key: 'fechaCreacion' },
    { 
      title: 'Progreso', 
      dataIndex: 'progreso', 
      key: 'progreso',
      render: (progreso: number) => `${progreso}%`
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'dibujo') color = 'blue';
        if (tipo === 'render') color = 'geekblue';
        if (tipo === 'simulacion') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EyeOutlined />}>Ver</Button>
          <Button type="link" icon={<DownloadOutlined />}>Descargar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearAgente = () => {
    setAgentModalVisible(true);
  };

  const handleVerTareas = () => {
    setTasksModalVisible(true);
  };

  const handleGuardarAgente = async () => {
    try {
      const values = await form.validateFields();
      message.success('Agente CAD creado exitosamente');
      setAgentModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear agente:', error);
      message.error('Error al crear el agente');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><ToolOutlined /> Agentes CAD</Title>
          <Text>
            Gestión de agentes CAD distribuidos para reducir la carga del servidor principal
          </Text>
        </div>
        <Space>
          <Button icon={<DeploymentUnitOutlined />} onClick={handleVerTareas}>
            Ver Tareas
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCrearAgente}>
            Nuevo Agente
          </Button>
        </Space>
      </Row>

      <Alert
        message="Importante"
        description="Los agentes CAD distribuyen la carga de procesamiento gráfico y geométrico, mejorando el rendimiento del sistema."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card className="dashboard-card">
        <Table 
          dataSource={agentsData} 
          columns={columnasAgentes} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="Crear Nuevo Agente CAD"
        open={agentModalVisible}
        onCancel={() => {
          setAgentModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarAgente}
        >
          <Form.Item name="nombre" label="Nombre del Agente" rules={[{ required: true, message: 'Ingrese el nombre del agente' }]}>
            <Input placeholder="Ej: Agente Renderizado Principal" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Agente" rules={[{ required: true, message: 'Seleccione el tipo de agente' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="dibujo">Dibujo Técnico</Option>
                  <Option value="render">Renderizado</Option>
                  <Option value="simulacion">Simulación</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="estado" label="Estado Inicial" rules={[{ required: true, message: 'Seleccione el estado inicial' }]}>
                <Select placeholder="Seleccione el estado">
                  <Option value="activo">Activo</Option>
                  <Option value="inactivo">Inactivo</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="capacidad" label="Capacidad de Procesamiento" rules={[{ required: true, message: 'Ingrese la capacidad del agente' }]}>
            <Input placeholder="Ej: 8 núcleos, 16GB RAM, GPU RTX 3080" />
          </Form.Item>
          
          <Form.Item name="ubicacion" label="Ubicación Física">
            <Input placeholder="Ej: Estación de Diseño 1, Servidor Local" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del agente y su propósito" rows={3} />
          </Form.Item>
          
          <Form.Item name="requiereAutenticacion" label="Requiere Autenticación" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
          
          <Form.Item name="permiteRenderRemoto" label="Permite Renderizado Remoto" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setAgentModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Agente
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Tareas CAD"
        open={tasksModalVisible}
        onCancel={() => setTasksModalVisible(false)}
        footer={null}
        width={900}
      >
        <Table 
          dataSource={tasksData} 
          columns={columnasTareas} 
          pagination={{ pageSize: 10 }}
        />
      </Modal>
    </div>
  );
};

export default CADAgents;