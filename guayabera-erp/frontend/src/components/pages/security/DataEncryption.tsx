import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  LockOutlined,
  SafetyCertificateOutlined,
  KeyOutlined,
  DatabaseOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  FileProtectOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const DataEncryption: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('encryption');
  const [form] = Form.useForm();
  
  // Datos simulados para campos encriptados
  const encryptedFieldsData = [
    { id: '1', tabla: 'clientes', campo: 'email', tipo: 'email', estado: 'activo', algoritmo: 'AES-256-GCM', fecha_inicio: '2023-01-15' },
    { id: '2', tabla: 'clientes', campo: 'telefono', tipo: 'telefono', estado: 'activo', algoritmo: 'AES-256-GCM', fecha_inicio: '2023-01-15' },
    { id: '3', tabla: 'empleados', campo: 'rfc', tipo: 'rfc', estado: 'activo', algoritmo: 'AES-256-GCM', fecha_inicio: '2023-02-01' },
    { id: '4', tabla: 'empleados', campo: 'curp', tipo: 'curp', estado: 'activo', algoritmo: 'AES-256-GCM', fecha_inicio: '2023-02-01' },
  ];

  // Datos simulados para algoritmos de encriptación
  const algorithmData = [
    { id: '1', nombre: 'AES-256-GCM', descripcion: 'Advanced Encryption Standard con Galois/Counter Mode', seguridad: 95, estado: 'activo' },
    { id: '2', nombre: 'RSA-4096', descripcion: 'Criptosistema de clave pública RSA con 4096 bits', seguridad: 90, estado: 'activo' },
    { id: '3', nombre: 'ChaCha20-Poly1305', descripcion: 'Algoritmo de cifrado de flujo con autenticación', seguridad: 85, estado: 'inactivo' },
  ];

  const columnasCampos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Tabla', dataIndex: 'tabla', key: 'tabla' },
    { title: 'Campo', dataIndex: 'campo', key: 'campo' },
    { title: 'Tipo de Dato', dataIndex: 'tipo', key: 'tipo' },
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
    { title: 'Algoritmo', dataIndex: 'algoritmo', key: 'algoritmo' },
    { title: 'Fecha Inicio', dataIndex: 'fecha_inicio', key: 'fecha_inicio' },
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

  const columnasAlgoritmos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Nivel de Seguridad', 
      dataIndex: 'seguridad', 
      key: 'seguridad',
      render: (seguridad: number) => (
        <div>
          <Progress percent={seguridad} size="small" />
          <Text>{seguridad}%</Text>
        </div>
      )
    },
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

  const handleCrearCampo = () => {
    setModalVisible(true);
  };

  const handleGuardarCampo = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear campo encriptado:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><LockOutlined /> Encriptación de Datos</Title>
          <Text>
            Protección de información sensible tanto en tránsito como en reposo
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearCampo}>
            Nuevo Campo
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Campos Encriptados"
              value={24}
              prefix={<DatabaseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Algoritmos Activos"
              value={3}
              prefix={<KeyOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Nivel de Seguridad"
              value={95}
              precision={0}
              suffix="%"
              prefix={<SafetyCertificateOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Datos Protegidos"
              value={87500}
              prefix={<FileProtectOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="encryption" onChange={setActiveTab}>
        <TabPane tab="Campos Encriptados" key="encryption">
          <Card className="dashboard-card">
            <Table 
              dataSource={encryptedFieldsData} 
              columns={columnasCampos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Algoritmos de Encriptación" key="algorithms">
          <Card className="dashboard-card">
            <Table 
              dataSource={algorithmData} 
              columns={columnasAlgoritmos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Agregar Campo para Encriptación"
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
          onFinish={handleGuardarCampo}
        >
          <Form.Item name="tabla" label="Tabla" rules={[{ required: true, message: 'Seleccione la tabla' }]}>
            <Select placeholder="Seleccione la tabla">
              <Option value="clientes">Clientes</Option>
              <Option value="empleados">Empleados</Option>
              <Option value="proveedores">Proveedores</Option>
              <Option value="usuarios">Usuarios</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="campo" label="Campo" rules={[{ required: true, message: 'Ingrese el nombre del campo' }]}>
            <Input placeholder="Ej: email, telefono, rfc" />
          </Form.Item>
          
          <Form.Item name="tipo" label="Tipo de Dato" rules={[{ required: true, message: 'Seleccione el tipo de dato' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="email">Email</Option>
              <Option value="telefono">Teléfono</Option>
              <Option value="direccion">Dirección</Option>
              <Option value="rfc">RFC</Option>
              <Option value="curp">CURP</Option>
              <Option value="clave">Clave/Contraseña</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del campo y su propósito" rows={4} />
          </Form.Item>
          
          <Form.Item name="algoritmo" label="Algoritmo de Encriptación" rules={[{ required: true, message: 'Seleccione el algoritmo' }]}>
            <Select placeholder="Seleccione el algoritmo">
              <Option value="aes256gcm">AES-256-GCM</Option>
              <Option value="rsa4096">RSA-4096</Option>
              <Option value="chacha20poly1305">ChaCha20-Poly1305</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="nivel_seguridad" label="Nivel de Seguridad Requerido" rules={[{ required: true, message: 'Seleccione el nivel de seguridad' }]}>
            <Select placeholder="Seleccione el nivel">
              <Option value="bajo">Bajo (70-79%)</Option>
              <Option value="medio">Medio (80-89%)</Option>
              <Option value="alto">Alto (90-95%)</Option>
              <Option value="muy_alto">Muy Alto (96-100%)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="estado" label="Estado" rules={[{ required: true, message: 'Seleccione el estado' }]}>
            <Select placeholder="Seleccione el estado">
              <Option value="activo">Activo</Option>
              <Option value="inactivo">Inactivo</Option>
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
                Agregar Campo
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default DataEncryption;