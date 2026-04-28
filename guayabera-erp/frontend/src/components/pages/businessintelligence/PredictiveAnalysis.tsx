import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, message } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  BarChartOutlined,
  ThunderboltOutlined,
  PlayCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const PredictiveAnalysis: React.FC = () => {
  const [analysisModalVisible, setAnalysisModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para análisis predictivos
  const analysisData = [
    { id: '1', nombre: 'Predicción de Ventas Q3', modelo: 'Regresión Lineal', precision: 92.5, autor: 'Carlos Gómez', ultima_ejecucion: '2023-04-15', activo: true },
    { id: '2', nombre: 'Demanda de Productos', modelo: 'Series Temporales', precision: 87.3, autor: 'Ana Martínez', ultima_ejecucion: '2023-04-14', activo: true },
    { id: '3', nombre: 'Retención de Clientes', modelo: 'Clasificación', precision: 89.7, autor: 'María López', ultima_ejecucion: '2023-04-13', activo: false },
    { id: '4', nombre: 'Inventario Óptimo', modelo: 'Machine Learning', precision: 95.2, autor: 'Juan Pérez', ultima_ejecucion: '2023-04-12', activo: true },
  ];

  const columnasAnalisis = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Modelo', 
      dataIndex: 'modelo', 
      key: 'modelo',
      render: (modelo: string) => {
        let color = 'default';
        if (modelo === 'Regresión Lineal') color = 'blue';
        if (modelo === 'Series Temporales') color = 'green';
        if (modelo === 'Clasificación') color = 'orange';
        if (modelo === 'Machine Learning') color = 'purple';
        return <Tag color={color}>{modelo}</Tag>;
      }
    },
    { 
      title: 'Precisión', 
      dataIndex: 'precision', 
      key: 'precision',
      render: (precision: number) => `${precision}%`
    },
    { title: 'Autor', dataIndex: 'autor', key: 'autor' },
    { title: 'Última Ejecución', dataIndex: 'ultima_ejecucion', key: 'ultima_ejecucion' },
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
          <Button type="link" icon={<PlayCircleOutlined />}>Ejecutar</Button>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearAnalisis = () => {
    setAnalysisModalVisible(true);
  };

  const handleGuardarAnalisis = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      message.success('Análisis predictivo creado exitosamente');
      setAnalysisModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear análisis:', error);
      message.error('Error al crear el análisis');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><ThunderboltOutlined /> Análisis Predictivo</Title>
          <Text>
            Creación y gestión de modelos predictivos para anticipar tendencias y comportamientos
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearAnalisis}>
            Nuevo Análisis
          </Button>
        </Space>
      </Row>

      <Card className="dashboard-card">
        <Table 
          dataSource={analysisData} 
          columns={columnasAnalisis} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="Crear Nuevo Análisis Predictivo"
        open={analysisModalVisible}
        onCancel={() => {
          setAnalysisModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarAnalisis}
        >
          <Form.Item name="nombre" label="Nombre del Análisis" rules={[{ required: true, message: 'Ingrese el nombre del análisis' }]}>
            <Input placeholder="Ej: Predicción de Demanda de Productos" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del análisis y su propósito" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo_modelo" label="Tipo de Modelo" rules={[{ required: true, message: 'Seleccione el tipo de modelo' }]}>
                <Select placeholder="Seleccione el tipo de modelo">
                  <Option value="regresion_lineal">Regresión Lineal</Option>
                  <Option value="series_temporales">Series Temporales</Option>
                  <Option value="clasificacion">Clasificación</Option>
                  <Option value="machine_learning">Machine Learning</Option>
                  <Option value="red_neuronal">Red Neuronal</Option>
                  <Option value="arbol_decision">Árbol de Decisión</Option>
                </Select>
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
          
          <Tabs defaultActiveKey="formula">
            <TabPane tab={<><ThunderboltOutlined /> Fórmula del Modelo</>} key="formula">
              <Form.Item 
                name="formula" 
                label="Fórmula del Modelo" 
                rules={[{ required: true, message: 'Ingrese la fórmula del modelo' }]}
              >
                <TextArea 
                  placeholder={`Ejemplo de fórmula para predicción de ventas:
y = β₀ + β₁*x₁ + β₂*x₂ + ... + βₙ*xₙ

Donde:
- y: Variable objetivo (ventas)
- x₁, x₂, ..., xₙ: Variables predictoras (precio, temporada, promociones, etc.)
- β₀, β₁, ..., βₙ: Coeficientes del modelo`} 
                  rows={8} 
                />
              </Form.Item>
            </TabPane>
            
            <TabPane tab={<><BarChartOutlined /> Configuración</>} key="config">
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="frecuencia_entrenamiento" label="Frecuencia de Entrenamiento">
                    <Select placeholder="Seleccionar frecuencia">
                      <Option value="diario">Diario</Option>
                      <Option value="semanal">Semanal</Option>
                      <Option value="quincenal">Quincenal</Option>
                      <Option value="mensual">Mensual</Option>
                      <Option value="trimestral">Trimestral</Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="variables_entrada" label="Variables de Entrada">
                    <Select 
                      mode="tags" 
                      placeholder="Ingrese las variables de entrada"
                      dropdownRender={() => null}
                    >
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="descripcion_variables" label="Descripción de Variables">
                <TextArea 
                  placeholder="Describa cada variable de entrada y su impacto esperado en la predicción" 
                  rows={4} 
                />
              </Form.Item>
            </TabPane>
          </Tabs>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setAnalysisModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Análisis
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default PredictiveAnalysis;