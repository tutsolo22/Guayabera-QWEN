import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Statistic, Image } from 'antd';
import { 
  ScanOutlined,
  QrcodeOutlined,
  BarcodeOutlined,
  SearchOutlined,
  AppstoreOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const QRScanner: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('scan');
  const [form] = Form.useForm();
  
  // Datos simulados para productos escaneados
  const scannedProductsData = [
    { id: '1', codigo: 'PROD-001', nombre: 'Camisa Casual', categoria: 'Ropa', ubicacion: 'Almacén A', fecha_escaneo: '2023-04-15 10:30:25', usuario: 'Carlos Gómez' },
    { id: '2', codigo: 'PROD-002', nombre: 'Pantalón Jeans', categoria: 'Ropa', ubicacion: 'Almacén B', fecha_escaneo: '2023-04-15 11:15:42', usuario: 'María López' },
    { id: '3', codigo: 'PROD-003', nombre: 'Vestido de Fiesta', categoria: 'Ropa', ubicacion: 'Almacén A', fecha_escaneo: '2023-04-15 12:05:18', usuario: 'Ana Martínez' },
    { id: '4', codigo: 'PROD-004', nombre: 'Chaqueta Formal', categoria: 'Ropa', ubicacion: 'Almacén C', fecha_escaneo: '2023-04-15 13:22:55', usuario: 'Luis Fernández' },
  ];

  // Datos simulados para ubicaciones
  const locationData = [
    { id: '1', codigo: 'ALM-A', nombre: 'Almacén A', capacidad: 500, ocupado: 320, estado: 'activo' },
    { id: '2', codigo: 'ALM-B', nombre: 'Almacén B', capacidad: 300, ocupado: 180, estado: 'activo' },
    { id: '3', codigo: 'ALM-C', nombre: 'Almacén C', capacidad: 400, ocupado: 250, estado: 'activo' },
    { id: '4', codigo: 'ALM-D', nombre: 'Área de Producción', capacidad: 200, ocupado: 150, estado: 'activo' },
  ];

  const columnasProductos = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Categoría', dataIndex: 'categoria', key: 'categoria' },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { title: 'Fecha Escaneo', dataIndex: 'fecha_escaneo', key: 'fecha_escaneo' },
    { title: 'Usuario', dataIndex: 'usuario', key: 'usuario' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<SearchOutlined />}>Detalles</Button>
          <Button type="link" icon={<FileTextOutlined />}>Inventario</Button>
        </Space>
      ),
    },
  ];

  const columnasUbicaciones = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Capacidad', dataIndex: 'capacidad', key: 'capacidad' },
    { title: 'Ocupado', dataIndex: 'ocupado', key: 'ocupado' },
    { 
      title: 'Disponible', 
      key: 'disponible',
      render: (record: any) => record.capacidad - record.ocupado
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
          <Button type="link" icon={<SearchOutlined />}>Ver Detalles</Button>
          <Button type="link" icon={<AppstoreOutlined />}>Inventario</Button>
        </Space>
      ),
    },
  ];

  const handleCrearQR = () => {
    setModalVisible(true);
  };

  const handleGuardarQR = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al generar código QR:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><QrcodeOutlined /> Escaneo de Códigos QR</Title>
          <Text>
            Inventario y localización de productos mediante escáner de códigos QR
          </Text>
        </div>
        <Space>
          <Button icon={<ScanOutlined />} type="primary">
            Iniciar Escaneo
          </Button>
          <Button icon={<PlusOutlined />} onClick={handleCrearQR}>
            Generar Código QR
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Productos Escaneados"
              value={1248}
              prefix={<QrcodeOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Ubicaciones"
              value={12}
              prefix={<AppstoreOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Usuarios Activos"
              value={24}
              prefix={<SearchOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Códigos Generados"
              value={356}
              prefix={<BarcodeOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="scan" onChange={setActiveTab}>
        <TabPane tab="Escaneo de Productos" key="scan">
          <Card className="dashboard-card">
            <Table 
              dataSource={scannedProductsData} 
              columns={columnasProductos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Ubicaciones" key="locations">
          <Card className="dashboard-card">
            <Table 
              dataSource={locationData} 
              columns={columnasUbicaciones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Generar Código QR"
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
          onFinish={handleGuardarQR}
        >
          <Form.Item name="tipo_elemento" label="Tipo de Elemento" rules={[{ required: true, message: 'Seleccione el tipo de elemento' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="producto">Producto</Option>
              <Option value="ubicacion">Ubicación</Option>
              <Option value="equipo">Equipo</Option>
              <Option value="documento">Documento</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="elemento_id" label="ID del Elemento" rules={[{ required: true, message: 'Ingrese el ID del elemento' }]}>
            <Input placeholder="Ej: PROD-001, ALM-A, EQP-001" />
          </Form.Item>
          
          <Form.Item name="nombre_elemento" label="Nombre del Elemento" rules={[{ required: true, message: 'Ingrese el nombre del elemento' }]}>
            <Input placeholder="Ej: Camisa Casual, Almacén A, Máquina de Coser" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del elemento" rows={4} />
          </Form.Item>
          
          <Form.Item name="datos_extra" label="Datos Extra">
            <Select 
              mode="tags" 
              placeholder="Agregue datos adicionales a incluir en el QR"
              dropdownRender={() => null}
            >
            </Select>
          </Form.Item>
          
          <Form.Item label="Vista Previa del Código QR">
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <Image
                width={200}
                src="https://placehold.co/200x200?text=Código+QR"
                alt="Vista previa del código QR generado"
              />
              <Text type="secondary" style={{ display: 'block', marginTop: '10px' }}>
                Vista previa del código QR generado
              </Text>
            </div>
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
              <Button type="primary" htmlType="submit" icon={<QrcodeOutlined />}>
                Generar Código QR
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default QRScanner;