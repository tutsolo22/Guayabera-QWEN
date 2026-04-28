import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  SignatureOutlined,
  FileDoneOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  UserOutlined,
  FileTextOutlined,
  SendOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const ElectronicSignatures: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('signatures');
  const [form] = Form.useForm();
  
  // Datos simulados para solicitudes de firma
  const signatureRequestData = [
    { id: '1', documento: 'Contrato Empleado', tipo: 'contrato', estado: 'pendiente', solicitante: 'Carlos Gómez', fecha_solicitud: '2023-04-15', firmas_restantes: 2 },
    { id: '2', documento: 'Solicitud Compra', tipo: 'compra', estado: 'firmado', solicitante: 'María López', fecha_solicitud: '2023-04-14', firmas_restantes: 0 },
    { id: '3', documento: 'Acuerdo Confidencial', tipo: 'legal', estado: 'en_proceso', solicitante: 'Ana Martínez', fecha_solicitud: '2023-04-12', firmas_restantes: 1 },
    { id: '4', documento: 'Política Seguridad', tipo: 'interna', estado: 'rechazado', solicitante: 'Luis Fernández', fecha_solicitud: '2023-04-10', firmas_restantes: 0 },
  ];

  // Datos simulados para firmas guardadas
  const savedSignatureData = [
    { id: '1', nombre: 'Carlos Gómez', cargo: 'Director General', estado: 'activo', fecha_registro: '2023-01-15', uso: 42 },
    { id: '2', nombre: 'María López', cargo: 'Gerente Finanzas', estado: 'activo', fecha_registro: '2023-02-01', uso: 28 },
    { id: '3', nombre: 'Ana Martínez', cargo: 'Jefa de Recursos Humanos', estado: 'activo', fecha_registro: '2023-02-10', uso: 15 },
    { id: '4', nombre: 'Luis Fernández', cargo: 'Coordinador de Compras', estado: 'inactivo', fecha_registro: '2023-03-05', uso: 8 },
  ];

  const columnasSolicitudes = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Documento', dataIndex: 'documento', key: 'documento' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'contrato') color = 'blue';
        if (tipo === 'compra') color = 'green';
        if (tipo === 'legal') color = 'red';
        if (tipo === 'interna') color = 'orange';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'en_proceso') color = 'blue';
        if (estado === 'firmado') color = 'green';
        if (estado === 'rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Solicitante', dataIndex: 'solicitante', key: 'solicitante' },
    { title: 'Fecha Solicitud', dataIndex: 'fecha_solicitud', key: 'fecha_solicitud' },
    { title: 'Firmas Restantes', dataIndex: 'firmas_restantes', key: 'firmas_restantes' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<SendOutlined />}>Enviar</Button>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Cancelar</Button>
        </Space>
      ),
    },
  ];

  const columnasFirmas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Cargo', dataIndex: 'cargo', key: 'cargo' },
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
    { title: 'Fecha Registro', dataIndex: 'fecha_registro', key: 'fecha_registro' },
    { title: 'Usos', dataIndex: 'uso', key: 'uso' },
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

  const handleCrearSolicitud = () => {
    setModalVisible(true);
  };

  const handleGuardarSolicitud = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear solicitud de firma:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><SignatureOutlined /> Firmas Electrónicas</Title>
          <Text>
            Validación de operaciones mediante firma digital
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearSolicitud}>
            Nueva Solicitud
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Solicitudes"
              value={124}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Firmas Completadas"
              value={87}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Firmas Guardadas"
              value={24}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Rechazadas"
              value={8}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="signatures" onChange={setActiveTab}>
        <TabPane tab="Solicitudes de Firma" key="signatures">
          <Card className="dashboard-card">
            <Table 
              dataSource={signatureRequestData} 
              columns={columnasSolicitudes} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Firmas Guardadas" key="saved">
          <Card className="dashboard-card">
            <Table 
              dataSource={savedSignatureData} 
              columns={columnasFirmas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Solicitud de Firma Electrónica"
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
          onFinish={handleGuardarSolicitud}
        >
          <Form.Item name="documento" label="Documento" rules={[{ required: true, message: 'Seleccione el documento' }]}>
            <Select placeholder="Seleccione el documento">
              <Option value="contrato_empleado">Contrato de Empleado</Option>
              <Option value="solicitud_compra">Solicitud de Compra</Option>
              <Option value="acuerdo_confidencial">Acuerdo de Confidencialidad</Option>
              <Option value="política_seguridad">Política de Seguridad</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="tipo_documento" label="Tipo de Documento" rules={[{ required: true, message: 'Seleccione el tipo de documento' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="contrato">Contrato</Option>
              <Option value="compra">Compra</Option>
              <Option value="legal">Legal</Option>
              <Option value="interno">Interno</Option>
              <Option value="externo">Externo</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del documento y propósito de la firma" rows={4} />
          </Form.Item>
          
          <Form.Item name="firmantes" label="Firmantes" rules={[{ required: true, message: 'Seleccione al menos un firmante' }]}>
            <Select 
              mode="multiple" 
              placeholder="Seleccione los firmantes"
            >
              <Option value="director_general">Carlos Gómez - Director General</Option>
              <Option value="gerente_finanzas">María López - Gerente Finanzas</Option>
              <Option value="jefa_rh">Ana Martínez - Jefa de RH</Option>
              <Option value="coordinador_compras">Luis Fernández - Coordinador Compras</Option>
              <Option value="representante_legal">Pedro Ramírez - Representante Legal</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="prioridad" label="Prioridad" rules={[{ required: true, message: 'Seleccione la prioridad' }]}>
            <Select placeholder="Seleccione la prioridad">
              <Option value="normal">Normal</Option>
              <Option value="alta">Alta</Option>
              <Option value="urgente">Urgente</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="vencimiento" label="Fecha de Vencimiento">
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="notificaciones" label="Notificaciones">
            <Select 
              mode="multiple" 
              placeholder="Seleccione métodos de notificación"
            >
              <Option value="email">Correo Electrónico</Option>
              <Option value="sms">SMS</Option>
              <Option value="sistema">Notificación Interna</Option>
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
                Crear Solicitud
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ElectronicSignatures;