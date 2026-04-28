import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, InputNumber, Slider } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  DollarOutlined,
  TeamOutlined,
  PercentageOutlined,
  UsergroupAddOutlined,
  ShoppingOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const ClientLevelPricing: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [discountModalVisible, setDiscountModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('levels');
  const [form] = Form.useForm();
  const [discountForm] = Form.useForm();
  
  // Datos simulados para niveles de cliente
  const levelData = [
    { id: '1', nombre: 'Platino', descripcion: 'Clientes premium con mayores volúmenes', descuento: 25, min_compra: 50000, activo: true },
    { id: '2', nombre: 'Oro', descripcion: 'Clientes con compras regulares', descuento: 15, min_compra: 25000, activo: true },
    { id: '3', nombre: 'Plata', descripcion: 'Clientes nuevos o con compras moderadas', descuento: 10, min_compra: 10000, activo: true },
    { id: '4', nombre: 'Bronce', descripcion: 'Clientes ocasionales', descuento: 5, min_compra: 0, activo: true },
  ];

  // Datos simulados para precios especiales por cliente
  const specialPriceData = [
    { id: '1', cliente: 'Moda S.A.', producto: 'Camisa Casual', precio: 400, vigencia_inicio: '2023-01-01', vigencia_fin: '2023-12-31', estado: 'activo' },
    { id: '2', cliente: 'Tendencias SA', producto: 'Pantalón Jeans', precio: 750, vigencia_inicio: '2023-03-01', vigencia_fin: '2023-08-31', estado: 'activo' },
    { id: '3', cliente 'Distribuciones XYZ', producto: 'Vestido de Fiesta', precio: 1200, vigencia_inicio: '2023-02-15', vigencia_fin: '2023-07-15', estado: 'expirado' },
  ];

  const columnasNiveles = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Descuento', 
      dataIndex: 'descuento', 
      key: 'descuento',
      render: (descuento: number) => `${descuento}%`
    },
    { 
      title: 'Compra Mínima', 
      dataIndex: 'min_compra', 
      key: 'min_compra',
      render: (min_compra: number) => `$${min_compra.toLocaleString()}`
    },
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

  const columnasPrecios = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { 
      title: 'Precio', 
      dataIndex: 'precio', 
      key: 'precio',
      render: (precio: number) => `$${precio.toLocaleString()}`
    },
    { title: 'Vigencia Inicio', dataIndex: 'vigencia_inicio', key: 'vigencia_inicio' },
    { title: 'Vigencia Fin', dataIndex: 'vigencia_fin', key: 'vigencia_fin' },
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
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearNivel = () => {
    setModalVisible(true);
  };

  const handleCrearPrecio = () => {
    setDiscountModalVisible(true);
  };

  const handleGuardarNivel = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear nivel:', error);
    }
  };

  const handleGuardarPrecio = async () => {
    try {
      const values = await discountForm.validateFields();
      console.log('Valores del formulario:', values);
      setDiscountModalVisible(false);
      discountForm.resetFields();
    } catch (error) {
      console.error('Error al crear precio especial:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><DollarOutlined /> Precios por Niveles de Cliente</Title>
          <Text>
            Definición de descuentos progresivos según volumen de compras y precios especiales por cliente
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'levels' ? handleCrearNivel : handleCrearPrecio}>
            Nuevo {activeTab === 'levels' ? 'Nivel' : 'Precio Especial'}
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="levels" onChange={setActiveTab}>
        <TabPane tab="Niveles de Cliente" key="levels">
          <Card className="dashboard-card">
            <Table 
              dataSource={levelData} 
              columns={columnasNiveles} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Precios Especiales" key="specialPrices">
          <Card className="dashboard-card">
            <Table 
              dataSource={specialPriceData} 
              columns={columnasPrecios} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Nivel de Cliente"
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
          onFinish={handleGuardarNivel}
        >
          <Form.Item name="nombre" label="Nombre del Nivel" rules={[{ required: true, message: 'Ingrese el nombre del nivel' }]}>
            <Input placeholder="Ej: Platino, Oro, Plata, etc." />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del nivel y beneficios" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="descuento" label="Porcentaje de Descuento" rules={[{ required: true, message: 'Ingrese el porcentaje de descuento' }]}>
                <Slider 
                  min={0} 
                  max={100} 
                  tooltip={{ formatter: (value) => `${value}%` }}
                  marks={{ 0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="descuento_valor" label="Valor del Descuento" rules={[{ required: true, message: 'Ingrese el valor del descuento' }]}>
                <InputNumber 
                  min={0} 
                  max={100} 
                  formatter={value => `${value}%`}
                  parser={value => value!.replace('%', '')}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="min_compra" label="Compra Mínima Requerida" rules={[{ required: true, message: 'Ingrese la compra mínima requerida' }]}>
            <InputNumber 
              placeholder="Monto mínimo de compra para acceder a este nivel"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item name="activo" label="Estado" valuePropName="checked">
            <Select placeholder="Seleccione el estado">
              <Option value={true}>Activo</Option>
              <Option value={false}>Inactivo</Option>
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
                Crear Nivel
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Crear Precio Especial para Cliente"
        open={discountModalVisible}
        onCancel={() => {
          setDiscountModalVisible(false);
          discountForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={discountForm}
          layout="vertical"
          onFinish={handleGuardarPrecio}
        >
          <Form.Item name="cliente" label="Cliente" rules={[{ required: true, message: 'Seleccione el cliente' }]}>
            <Select placeholder="Seleccione el cliente">
              <Option value="moda_sa">Moda S.A.</Option>
              <Option value="tendencias_sa">Tendencias SA</Option>
              <Option value="distribuciones_xyz">Distribuciones XYZ</Option>
              <Option value="ropa_al_por_mayor">Ropa al Por Mayor</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="producto" label="Producto" rules={[{ required: true, message: 'Seleccione el producto' }]}>
            <Select placeholder="Seleccione el producto">
              <Option value="camisa_casual">Camisa Casual</Option>
              <Option value="pantalon_jeans">Pantalón Jeans</Option>
              <Option value="vestido_fiesta">Vestido de Fiesta</Option>
              <Option value="chaqueta_formal">Chaqueta Formal</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="precio" label="Precio Especial" rules={[{ required: true, message: 'Ingrese el precio especial' }]}>
            <InputNumber 
              placeholder="Precio especial para este cliente"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="vigencia_inicio" label="Vigencia Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="vigencia_fin" label="Vigencia Fin" rules={[{ required: true, message: 'Seleccione la fecha de fin' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="motivo" label="Motivo del Precio Especial">
            <TextArea placeholder="Razón por la cual se otorga este precio especial" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setDiscountModalVisible(false);
                discountForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Precio Especial
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ClientLevelPricing;