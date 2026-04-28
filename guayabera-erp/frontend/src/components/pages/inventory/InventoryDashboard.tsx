import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, Cascader, DatePicker, InputNumber, Tabs, Divider, message } from 'antd';
import { 
  PlusOutlined, 
  FileTextOutlined, 
  ShoppingCartOutlined, 
  DatabaseOutlined, 
  BoxPlotOutlined,
  SearchOutlined,
  TeamOutlined,
  FileSearchOutlined
} from '@ant-design/icons';
import { inventoryApi, BusquedaProductoTextil, ResultadoBusquedaProducto } from '../../../services/inventoryApi';
import TomaInventario from './TomaInventario';

// Definir las interfaces localmente
interface BusquedaProductoTextil {
  modelo?: string;
  color?: string;
  talla?: string;
  almacen_id?: string;
  empresa_id?: string;
  categoria_producto?: string;
  codigo_producto?: string;
  nombre_producto?: string;
  sobrenombre_1?: string;
  sobrenombre_2?: string;
}

interface ResultadoBusquedaProducto {
  producto_id: string;
  codigo_producto: string;
  nombre_producto: string;
  modelo?: string;
  color?: string;
  talla?: string;
  almacen_id: string;
  almacen_nombre: string;
  empresa_id?: string;
  empresa_nombre?: string;
  cantidad_disponible: number;
  categoria_producto?: string;
  sobrenombre_1?: string;
  sobrenombre_2?: string;
}

const { Title } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const InventoryDashboard: React.FC = () => {
  const [busquedaAvanzadaVisible, setBusquedaAvanzadaVisible] = useState(false);
  const [busquedaForm] = Form.useForm();
  const [resultadosBusqueda, setResultadosBusqueda] = useState<ResultadoBusquedaProducto[]>([]);
  const [busquedaRealizada, setBusquedaRealizada] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // Datos simulados para la tabla de productos
  const productosData = [
    { key: '1', id: 'PROD-001', codigo: 'CAM-GUA-AZUL-M', nombre: 'Camisa Guayabera Azul Marino', modelo: 'Guayabera', color: 'Azul Marino', talla: 'M', almacen: 'Principal', empresa: 'Matriz', cantidad: 45, categoria: 'Producto Terminado', sobrenombre1: 'Marino' },
    { key: '2', id: 'PROD-002', codigo: 'CAM-GUA-BLANCA-L', nombre: 'Camisa Guayabera Blanca', modelo: 'Guayabera', color: 'Blanco', talla: 'L', almacen: 'Secundario', empresa: 'Sucursal Norte', cantidad: 32, categoria: 'Producto Terminado', sobrenombre2: 'Crudo' },
    { key: '3', id: 'PROD-003', codigo: 'PANT-JEAN-NEGRO-32', nombre: 'Jean Negro Slim Fit', modelo: 'Jean', color: 'Negro', talla: '32', almacen: 'Principal', empresa: 'Matriz', cantidad: 28, categoria: 'Producto Terminado' },
    { key: '4', id: 'PROD-004', codigo: 'BLUSA-SILK-ROSA-M', nombre: 'Blusa Seda Rosa', modelo: 'Blusa', color: 'Rosado', talla: 'M', almacen: 'Principal', empresa: 'Matriz', cantidad: 15, categoria: 'Producto Terminado', sobrenombre1: 'Rosado Bebé' },
  ];

  const columnasProductos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Modelo', dataIndex: 'modelo', key: 'modelo' },
    { title: 'Color', dataIndex: 'color', key: 'color' },
    { title: 'Talla', dataIndex: 'talla', key: 'talla' },
    { 
      title: 'Almacén', 
      dataIndex: 'almacen', 
      key: 'almacen',
      render: (almacen: string) => <Tag color="blue">{almacen}</Tag>
    },
    { 
      title: 'Empresa', 
      dataIndex: 'empresa', 
      key: 'empresa',
      render: (empresa: string) => <Tag color="geekblue">{empresa}</Tag>
    },
    { 
      title: 'Cantidad', 
      dataIndex: 'cantidad', 
      key: 'cantidad',
      render: (cantidad: number) => <Tag color={cantidad < 20 ? 'red' : 'green'}>{cantidad}</Tag>
    },
    { 
      title: 'Categoría', 
      dataIndex: 'categoria', 
      key: 'categoria',
      render: (categoria: string) => <Tag color="purple">{categoria}</Tag>
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
          <Button type="link">Editar</Button>
        </Space>
      ),
    },
  ];

  // Columnas para resultados de búsqueda avanzada
  const columnasBusquedaAvanzada = [
    { title: 'Código Producto', dataIndex: 'codigo_producto', key: 'codigo_producto' },
    { title: 'Nombre Producto', dataIndex: 'nombre_producto', key: 'nombre_producto' },
    { title: 'Modelo', dataIndex: 'modelo', key: 'modelo' },
    { title: 'Color', dataIndex: 'color', key: 'color' },
    { title: 'Talla', dataIndex: 'talla', key: 'talla' },
    { 
      title: 'Almacén', 
      dataIndex: 'almacen_nombre', 
      key: 'almacen_nombre',
      render: (almacen_nombre: string) => <Tag color="blue">{almacen_nombre}</Tag>
    },
    { 
      title: 'Empresa', 
      dataIndex: 'empresa_nombre', 
      key: 'empresa_nombre',
      render: (empresa_nombre: string) => <Tag color="geekblue">{empresa_nombre}</Tag>
    },
    { 
      title: 'Cantidad Disponible', 
      dataIndex: 'cantidad_disponible', 
      key: 'cantidad_disponible',
      render: (cantidad: number) => <Tag color={cantidad < 20 ? 'red' : 'green'}>{cantidad}</Tag>
    },
    { 
      title: 'Categoría', 
      dataIndex: 'categoria_producto', 
      key: 'categoria_producto',
      render: (categoria: string) => <Tag color="purple">{categoria}</Tag>
    },
  ];

  const handleBuscarAvanzada = () => {
    setBusquedaAvanzadaVisible(true);
  };

  const handleBuscar = async () => {
    try {
      setLoading(true);
      const values = await busquedaForm.validateFields();
      
      // Transformar los valores del formulario al formato esperado por el API
      const busqueda: BusquedaProductoTextil = {
        modelo: values.modelo || undefined,
        color: values.color || undefined,
        talla: values.talla || undefined,
        almacen_id: values.almacen_id || undefined,
        empresa_id: values.empresa_id || undefined,
        categoria_producto: values.categoria_producto || undefined,
        codigo_producto: values.codigo_producto || undefined,
        nombre_producto: values.nombre_producto || undefined,
        sobrenombre_1: values.sobrenombre_1 || undefined,
        sobrenombre_2: values.sobrenombre_2 || undefined,
      };
      
      const response = await inventoryApi.buscarProductosTextilesAvanzada(busqueda);
      setResultadosBusqueda(response.resultados);
      setBusquedaRealizada(true);
      message.success(`Se encontraron ${response.total_resultados} productos`);
    } catch (error) {
      console.error('Error en la búsqueda:', error);
      message.error('Hubo un error al realizar la búsqueda');
    } finally {
      setLoading(false);
    }
  };

  const handleResetBusqueda = () => {
    busquedaForm.resetFields();
    setResultadosBusqueda([]);
    setBusquedaRealizada(false);
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Inventario</Title>
          <Typography.Text>
            Gestión de productos textiles, control de stock y ubicación de artículos
          </Typography.Text>
        </div>
        <Space>
          <Button type="primary" icon={<PlusOutlined />}>
            Nuevo Producto
          </Button>
          <Button icon={<SearchOutlined />} onClick={handleBuscarAvanzada}>
            Búsqueda Avanzada
          </Button>
          <Button icon={<FileSearchOutlined />} onClick={() => window.location.hash = "/inventory/toma-inventario"}>
            Toma de Inventario
          </Button>
        </Space>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Productos" 
              value={124} 
              prefix={<BoxPlotOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Categorías" 
              value={12} 
              prefix={<DatabaseOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Bajo Stock" 
              value={8} 
              prefix={<ShoppingCartOutlined />} 
              valueStyle={{ color: '#cf1322' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Almacenes" 
              value={4} 
              prefix={<TeamOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Tabs 
          defaultActiveKey="1" 
          items={[
            {
              label: 'Inventario Actual',
              key: '1',
              children: (
                <Table 
                  dataSource={productosData} 
                  columns={columnasProductos} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Movimientos',
              key: '2',
              children: <p>Movimientos de inventario</p>,
            },
            {
              label: 'Ajustes',
              key: '3',
              children: <p>Ajustes de inventario</p>,
            },
          ]} 
        />
      </Card>

      <Modal
        title="Búsqueda Avanzada de Productos Textiles"
        open={busquedaAvanzadaVisible}
        onCancel={() => {
          setBusquedaAvanzadaVisible(false);
          handleResetBusqueda();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={busquedaForm}
          layout="vertical"
          onFinish={handleBuscar}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="modelo" label="Modelo">
                <Input placeholder="Ej: Guayabera, Jean, Blusa" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="color" label="Color">
                <Input placeholder="Ej: Azul Marino, Blanco, Negro" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="talla" label="Talla">
                <Input placeholder="Ej: Chica, Mediana, Grande, 32, 34" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="categoria_producto" label="Categoría">
                <Select placeholder="Selecciona una categoría">
                  <Option value="producto_terminado">Producto Terminado</Option>
                  <Option value="tela">Tela</Option>
                  <Option value="avio">Avío</Option>
                  <Option value="insumo">Insumo</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="codigo_producto" label="Código de Producto">
                <Input placeholder="Código exacto del producto" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="nombre_producto" label="Nombre del Producto">
                <Input placeholder="Nombre parcial o completo del producto" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="sobrenombre_1" label="Sobrenombre 1">
                <Input placeholder="Primer sobrenombre para búsqueda" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="sobrenombre_2" label="Sobrenombre 2">
                <Input placeholder="Segundo sobrenombre para búsqueda" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="almacen_id" label="Almacén">
                <Select placeholder="Selecciona un almacén">
                  <Option value="">Todos los almacenes</Option>
                  <Option value="principal">Almacén Principal</Option>
                  <Option value="secundario">Almacén Secundario</Option>
                  <Option value="produccion">Almacén de Producción</Option>
                  <Option value="pv">Punto de Venta</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="empresa_id" label="Empresa (Multiempresa)">
                <Select placeholder="Selecciona una empresa">
                  <Option value="">Todas las empresas</Option>
                  <Option value="matriz">Matriz</Option>
                  <Option value="sucursal_norte">Sucursal Norte</Option>
                  <Option value="sucursal_sur">Sucursal Sur</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={handleResetBusqueda} loading={loading}>Limpiar</Button>
              <Button 
                type="primary" 
                htmlType="submit" 
                icon={<SearchOutlined />} 
                loading={loading}
              >
                Buscar
              </Button>
            </Space>
          </Row>
        </Form>
        
        {busquedaRealizada && (
          <div style={{ marginTop: 24 }}>
            <Title level={4}>Resultados de la Búsqueda</Title>
            <Table 
              dataSource={resultadosBusqueda} 
              columns={columnasBusquedaAvanzada} 
              pagination={{ pageSize: 10 }}
            />
          </div>
        )}
      </Modal>
    </div>
  );
};

export default InventoryDashboard;