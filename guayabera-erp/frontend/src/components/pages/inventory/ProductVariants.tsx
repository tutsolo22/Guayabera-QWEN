import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Upload, message } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  SkinOutlined,
  TagsOutlined,
  PictureOutlined,
  FileImageOutlined
} from '@ant-design/icons';
import { RcFile } from 'antd/lib/upload';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const ProductVariants: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [variantModalVisible, setVariantModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('products');
  const [form] = Form.useForm();
  const [variantForm] = Form.useForm();
  
  // Datos simulados para productos base
  const productData = [
    { id: '1', nombre: 'Camisa Casual', descripcion: 'Camisa casual de algodón', categoria: 'Camisas', marca: 'ModaSA', activo: true },
    { id: '2', nombre: 'Pantalón Jeans', descripcion: 'Pantalón jeans clásico', categoria: 'Pantalones', marca: 'DenimCo', activo: true },
    { id: '3', nombre: 'Vestido de Fiesta', descripcion: 'Vestido elegante para ocasiones especiales', categoria: 'Vestidos', marca: 'Elegance', activo: false },
  ];

  // Datos simulados para variantes
  const variantData = [
    { id: '1', producto: 'Camisa Casual', sku: 'CAM-CAS-S-AZ', talla: 'S', color: 'Azul', precio: 450, stock: 25, activo: true },
    { id: '2', producto: 'Camisa Casual', sku: 'CAM-CAS-M-AZ', talla: 'M', color: 'Azul', precio: 450, stock: 15, activo: true },
    { id: '3', producto: 'Camisa Casual', sku: 'CAM-CAS-L-RO', talla: 'L', color: 'Rojo', precio: 450, stock: 8, activo: true },
    { id: '4', producto: 'Pantalón Jeans', sku: 'PAN-JEA-M-BLA', talla: '32', color: 'Negro', precio: 850, stock: 12, activo: true },
  ];

  const columnasProductos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { title: 'Categoría', dataIndex: 'categoria', key: 'categoria' },
    { title: 'Marca', dataIndex: 'marca', key: 'marca' },
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
          <Button type="link" icon={<TagsOutlined />} onClick={() => {
            // Abrir modal de variantes para este producto
          }}>Variantes</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasVariantes = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'SKU', dataIndex: 'sku', key: 'sku' },
    { title: 'Talla', dataIndex: 'talla', key: 'talla' },
    { title: 'Color', dataIndex: 'color', key: 'color' },
    { 
      title: 'Precio', 
      dataIndex: 'precio', 
      key: 'precio',
      render: (precio: number) => `$${precio.toLocaleString()}`
    },
    { title: 'Stock', dataIndex: 'stock', key: 'stock' },
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
          <Button type="link" icon={<PictureOutlined />}>Imágenes</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearProducto = () => {
    setModalVisible(true);
  };

  const handleCrearVariante = () => {
    setVariantModalVisible(true);
  };

  const handleGuardarProducto = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
      message.success('Producto creado exitosamente');
    } catch (error) {
      console.error('Error al crear producto:', error);
      message.error('Error al crear el producto');
    }
  };

  const handleGuardarVariante = async () => {
    try {
      const values = await variantForm.validateFields();
      console.log('Valores del formulario de variante:', values);
      setVariantModalVisible(false);
      variantForm.resetFields();
      message.success('Variante creada exitosamente');
    } catch (error) {
      console.error('Error al crear variante:', error);
      message.error('Error al crear la variante');
    }
  };

  // Validador para el upload de imágenes
  const beforeUpload = (file: RcFile) => {
    const isImage = file.type.indexOf('image/') === 0;
    if (!isImage) {
      message.error('Solo puedes subir archivos de imagen!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('La imagen debe pesar menos de 2MB!');
    }
    return isImage && isLt2M;
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><SkinOutlined /> Catálogo de Productos Multivariante</Title>
          <Text>
            Gestión de combinaciones de talla/color/modelo para productos con múltiples variantes
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'products' ? handleCrearProducto : handleCrearVariante}>
            Nuevo {activeTab === 'products' ? 'Producto Base' : 'Variante'}
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="products" onChange={setActiveTab}>
        <TabPane tab="Productos Base" key="products">
          <Card className="dashboard-card">
            <Table 
              dataSource={productData} 
              columns={columnasProductos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Variantes de Productos" key="variants">
          <Card className="dashboard-card">
            <Table 
              dataSource={variantData} 
              columns={columnasVariantes} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Producto Base"
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
          onFinish={handleGuardarProducto}
        >
          <Form.Item name="nombre" label="Nombre del Producto" rules={[{ required: true, message: 'Ingrese el nombre del producto' }]}>
            <Input placeholder="Ej: Camisa Casual" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción detallada del producto" rows={4} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="categoria" label="Categoría" rules={[{ required: true, message: 'Seleccione la categoría' }]}>
                <Select placeholder="Seleccione la categoría">
                  <Option value="camisas">Camisas</Option>
                  <Option value="pantalones">Pantalones</Option>
                  <Option value="vestidos">Vestidos</Option>
                  <Option value="chaquetas">Chaquetas</Option>
                  <Option value="accesorios">Accesorios</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="marca" label="Marca" rules={[{ required: true, message: 'Seleccione la marca' }]}>
                <Select placeholder="Seleccione la marca">
                  <Option value="modasa">ModaSA</Option>
                  <Option value="denimco">DenimCo</Option>
                  <Option value="elegance">Elegance</Option>
                  <Option value="fashionplus">Fashion+</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="imagenes" label="Imágenes del Producto">
            <Upload 
              name="images" 
              listType="picture-card" 
              className="avatar-uploader"
              beforeUpload={beforeUpload}
              maxCount={5}
              accept="image/*"
            >
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <FileImageOutlined style={{ fontSize: '24px' }} />
                <div style={{ marginTop: 8 }}>Subir</div>
              </div>
            </Upload>
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
                Crear Producto
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Crear Nueva Variante de Producto"
        open={variantModalVisible}
        onCancel={() => {
          setVariantModalVisible(false);
          variantForm.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={variantForm}
          layout="vertical"
          onFinish={handleGuardarVariante}
        >
          <Form.Item name="producto" label="Producto Base" rules={[{ required: true, message: 'Seleccione el producto base' }]}>
            <Select placeholder="Seleccione el producto base">
              <Option value="camisa_casual">Camisa Casual</Option>
              <Option value="pantalon_jeans">Pantalón Jeans</Option>
              <Option value="vestido_fiesta">Vestido de Fiesta</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="sku" label="SKU" rules={[{ required: true, message: 'Ingrese el SKU' }]}>
            <Input placeholder="Ej: CAM-CAS-S-AZ" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="talla" label="Talla" rules={[{ required: true, message: 'Seleccione la talla' }]}>
                <Select placeholder="Seleccione la talla">
                  <Option value="xs">XS</Option>
                  <Option value="s">S</Option>
                  <Option value="m">M</Option>
                  <Option value="l">L</Option>
                  <Option value="xl">XL</Option>
                  <Option value="xxl">XXL</Option>
                  <Option value="32">32</Option>
                  <Option value="34">34</Option>
                  <Option value="36">36</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="color" label="Color" rules={[{ required: true, message: 'Seleccione el color' }]}>
                <Select placeholder="Seleccione el color">
                  <Option value="negro">Negro</Option>
                  <Option value="blanco">Blanco</Option>
                  <Option value="azul">Azul</Option>
                  <Option value="rojo">Rojo</Option>
                  <Option value="verde">Verde</Option>
                  <Option value="amarillo">Amarillo</Option>
                  <Option value="gris">Gris</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="precio" label="Precio de Venta" rules={[{ required: true, message: 'Ingrese el precio' }]}>
                <InputNumber 
                  placeholder="Precio del producto"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="stock" label="Stock Inicial" rules={[{ required: true, message: 'Ingrese el stock inicial' }]}>
                <InputNumber 
                  placeholder="Cantidad en stock"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="imagenes" label="Imágenes de la Variante">
            <Upload 
              name="variant_images" 
              listType="picture-card" 
              className="avatar-uploader"
              beforeUpload={beforeUpload}
              maxCount={5}
              accept="image/*"
            >
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <FileImageOutlined style={{ fontSize: '24px' }} />
                <div style={{ marginTop: 8 }}>Subir</div>
              </div>
            </Upload>
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
                setVariantModalVisible(false);
                variantForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Variante
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ProductVariants;