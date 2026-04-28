import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, Switch, Tabs, Divider, message, Alert } from 'antd';
import { 
  PrinterOutlined, 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  DeploymentUnitOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ThunderboltOutlined,
  ApiOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

interface PrintingAgent {
  key: string;
  id: string;
  nombre: string;
  estado: 'activo' | 'inactivo' | 'error';
  tipo: 'local' | 'red' | 'virtual';
  puerto: string;
  ubicacion: string;
  ultimaConexion: string;
  version: string;
}

interface PrintJob {
  key: string;
  id: string;
  nombreDocumento: string;
  agente: string;
  estado: 'pendiente' | 'imprimiendo' | 'completado' | 'fallido';
  fechaCreacion: string;
  paginas: number;
  copias: number;
}

const PrintingAgents: React.FC = () => {
  const [agentModalVisible, setAgentModalVisible] = useState(false);
  const [jobsModalVisible, setJobsModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para agentes de impresión
  const agentsData: PrintingAgent[] = [
    { key: '1', id: 'PA-001', nombre: 'Agente Impresora Principal', estado: 'activo', tipo: 'local', puerto: 'USB001', ubicacion: 'Oficina Central', ultimaConexion: '2023-04-18 10:30', version: '1.2.4' },
    { key: '2', id: 'PA-002', nombre: 'Agente Impresora Almacén', estado: 'activo', tipo: 'red', puerto: '192.168.1.100', ubicacion: 'Almacén Principal', ultimaConexion: '2023-04-18 09:45', version: '1.2.3' },
    { key: '3', id: 'PA-003', nombre: 'Agente PDF Virtual', estado: 'inactivo', tipo: 'virtual', puerto: 'VIRTUAL001', ubicacion: 'Servidor', ultimaConexion: '2023-04-17 16:20', version: '1.1.9' },
    { key: '4', id: 'PA-004', nombre: 'Agente Impresora Producción', estado: 'error', tipo: 'local', puerto: 'USB002', ubicacion: 'Área de Producción', ultimaConexion: '2023-04-18 08:15', version: '1.2.4' },
  ];

  // Datos simulados para trabajos de impresión
  const jobsData: PrintJob[] = [
    { key: '1', id: 'PJ-001', nombreDocumento: 'Reporte Ventas Abril', agente: 'Agente Impresora Principal', estado: 'completado', fechaCreacion: '2023-04-18 09:30', paginas: 12, copias: 2 },
    { key: '2', id: 'PJ-002', nombreDocumento: 'Etiquetas Producto Nuevo', agente: 'Agente Impresora Almacén', estado: 'imprimiendo', fechaCreacion: '2023-04-18 10:15', paginas: 4, copias: 50 },
    { key: '3', id: 'PJ-003', nombreDocumento: 'Constancia Nómina', agente: 'Agente Impresora Principal', estado: 'pendiente', fechaCreacion: '2023-04-18 10:45', paginas: 1, copias: 1 },
    { key: '4', id: 'PJ-004', nombreDocumento: 'Manual Usuario', agente: 'Agente PDF Virtual', estado: 'fallido', fechaCreacion: '2023-04-18 08:20', paginas: 45, copias: 1 },
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
        if (estado === 'error') color = 'red';
        return <Tag color={color}>{text}</Tag>;
      }
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'local') color = 'blue';
        if (tipo === 'red') color = 'geekblue';
        if (tipo === 'virtual') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Puerto', dataIndex: 'puerto', key: 'puerto' },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { title: 'Última Conexión', dataIndex: 'ultimaConexion', key: 'ultimaConexion' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
          <Button type="link" icon={<ThunderboltOutlined />}>Reiniciar</Button>
        </Space>
      ),
    },
  ];

  const columnasTrabajos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Documento', dataIndex: 'nombreDocumento', key: 'nombreDocumento' },
    { title: 'Agente', dataIndex: 'agente', key: 'agente' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        let text = estado;
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'imprimiendo') color = 'blue';
        if (estado === 'completado') color = 'green';
        if (estado === 'fallido') color = 'red';
        return <Tag color={color}>{text}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fechaCreacion', key: 'fechaCreacion' },
    { title: 'Páginas', dataIndex: 'paginas', key: 'paginas' },
    { title: 'Copias', dataIndex: 'copias', key: 'copias' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<CheckCircleOutlined />}>Reanudar</Button>
          <Button type="link" icon={<CloseCircleOutlined />} danger>Cancelar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearAgente = () => {
    setAgentModalVisible(true);
  };

  const handleVerTrabajos = () => {
    setJobsModalVisible(true);
  };

  const handleGuardarAgente = async () => {
    try {
      const values = await form.validateFields();
      message.success('Agente de impresión creado exitosamente');
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
          <Title level={2}><PrinterOutlined /> Agentes de Impresión</Title>
          <Text>
            Gestión de agentes de impresión locales y en red para reducir la carga del servidor
          </Text>
        </div>
        <Space>
          <Button icon={<DeploymentUnitOutlined />} onClick={handleVerTrabajos}>
            Ver Trabajos
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCrearAgente}>
            Nuevo Agente
          </Button>
        </Space>
      </Row>

      <Alert
        message="Importante"
        description="Los agentes de impresión se instalan en las máquinas locales para reducir la carga del servidor y mejorar la velocidad de impresión."
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
        title="Crear Nuevo Agente de Impresión"
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
            <Input placeholder="Ej: Agente Impresora Principal" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Agente" rules={[{ required: true, message: 'Seleccione el tipo de agente' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="local">Local (USB/Paralelo)</Option>
                  <Option value="red">Red (IP)</Option>
                  <Option value="virtual">Virtual (PDF)</Option>
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
          
          <Form.Item name="puerto" label="Puerto/Conexión" rules={[{ required: true, message: 'Ingrese el puerto o dirección IP' }]}>
            <Input placeholder="Ej: USB001 o 192.168.1.100" />
          </Form.Item>
          
          <Form.Item name="ubicacion" label="Ubicación Física">
            <Input placeholder="Ej: Oficina Central, Área de Producción" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del agente y su propósito" rows={3} />
          </Form.Item>
          
          <Form.Item name="requiereAutenticacion" label="Requiere Autenticación" valuePropName="checked" initialValue={true}>
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
        title="Trabajos de Impresión"
        open={jobsModalVisible}
        onCancel={() => setJobsModalVisible(false)}
        footer={null}
        width={900}
      >
        <Table 
          dataSource={jobsData} 
          columns={columnasTrabajos} 
          pagination={{ pageSize: 10 }}
        />
      </Modal>
    </div>
  );
};

export default PrintingAgents;