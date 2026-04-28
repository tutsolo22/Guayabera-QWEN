import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  BarChartOutlined,
  PercentageOutlined,
  RiseOutlined,
  FallOutlined,
  AlertOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { Column, ColumnConfig } from '@ant-design/plots';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const DeviationAnalysis: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('deviations');
  const [form] = Form.useForm();
  
  // Datos simulados para desviaciones
  const deviationData = [
    { id: '1', periodo: 'Ene 2023', cuenta: 'Ventas', real: 1250000, presupuesto: 1200000, desviacion: 50000, porcentaje: 4.2, estado: 'favorable', alerta: false },
    { id: '2', periodo: 'Ene 2023', cuenta: 'Costo Ventas', real: 750000, presupuesto: 700000, desviacion: 50000, porcentaje: 7.1, estado: 'desfavorable', alerta: true },
    { id: '3', periodo: 'Feb 2023', cuenta: 'Ventas', real: 1180000, presupuesto: 1250000, desviacion: -70000, porcentaje: -5.6, estado: 'desfavorable', alerta: true },
    { id: '4', periodo: 'Feb 2023', cuenta: 'Publicidad', real: 120000, presupuesto: 150000, desviacion: -30000, porcentaje: -20.0, estado: 'favorable', alerta: false },
  ];

  // Datos para gráfico de desviaciones
  const deviationGraphData = [
    { periodo: 'Ene 2023', cuenta: 'Ventas', desviacion: 4.2 },
    { periodo: 'Ene 2023', cuenta: 'Costo Ventas', desviacion: -7.1 },
    { periodo: 'Feb 2023', cuenta: 'Ventas', desviacion: -5.6 },
    { periodo: 'Feb 2023', cuenta: 'Publicidad', desviacion: -20.0 },
    { periodo: 'Mar 2023', cuenta: 'Ventas', desviacion: 2.3 },
    { periodo: 'Mar 2023', cuenta: 'Costo Ventas', desviacion: 3.1 },
  ];

  const columnasDesviaciones = [
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
    { title: 'Cuenta', dataIndex: 'cuenta', key: 'cuenta' },
    { 
      title: 'Real', 
      dataIndex: 'real', 
      key: 'real',
      render: (real: number) => `$${real.toLocaleString()}`
    },
    { 
      title: 'Presupuesto', 
      dataIndex: 'presupuesto', 
      key: 'presupuesto',
      render: (presupuesto: number) => `$${presupuesto.toLocaleString()}`
    },
    { 
      title: 'Desviación', 
      dataIndex: 'desviacion', 
      key: 'desviacion',
      render: (desviacion: number) => {
        const isPositive = desviacion >= 0;
        return (
          <Text type={isPositive ? 'success' : 'danger'}>
            {isPositive ? <RiseOutlined /> : <FallOutlined />} ${Math.abs(desviacion).toLocaleString()}
          </Text>
        );
      }
    },
    { 
      title: '% Desviación', 
      dataIndex: 'porcentaje', 
      key: 'porcentaje',
      render: (porcentaje: number) => {
        const isPositive = porcentaje >= 0;
        return (
          <Text type={isPositive ? 'success' : 'danger'}>
            {isPositive ? <RiseOutlined /> : <FallOutlined />} {Math.abs(porcentaje)}%
          </Text>
        );
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'favorable') color = 'green';
        if (estado === 'desfavorable') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { 
      title: 'Alerta', 
      dataIndex: 'alerta', 
      key: 'alerta',
      render: (alerta: boolean) => (
        alerta ? <Tag color="red"><AlertOutlined /> Sí</Tag> : <Tag color="default">No</Tag>
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

  // Configuración del gráfico de desviaciones
  const deviationConfig: ColumnConfig = {
    data: deviationGraphData,
    xField: 'periodo',
    yField: 'desviacion',
    seriesField: 'cuenta',
    isGroup: true,
    columnWidthRatio: 0.8,
    label: {
      position: 'top',
      style: {
        fill: '#FFFFFF',
        opacity: 0.6,
      },
    },
    yAxis: {
      nice: true,
    },
    legend: {
      position: 'top-left',
    },
    interactions: [
      {
        type: 'element-highlight-by-color',
      },
      {
        type: 'element-link',
      },
    ],
  };

  const handleCrearDesviacion = () => {
    setModalVisible(true);
  };

  const handleGuardarDesviacion = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear desviación:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><BarChartOutlined /> Análisis de Desviaciones</Title>
          <Text>
            Comparación entre valores reales y presupuestados con alertas para desviaciones significativas
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearDesviacion}>
            Nueva Desviación
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Desviaciones Mayores"
              value={12}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Con Alerta"
              value={8}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Favorables"
              value={15}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Desfavorables"
              value={7}
              prefix={<FallOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="deviations" onChange={setActiveTab}>
        <TabPane tab="Análisis de Desviaciones" key="deviations">
          <Card className="dashboard-card">
            <div style={{ height: 400 }}>
              <Column {...deviationConfig} />
            </div>
            <div style={{ marginTop: 24 }}>
              <Text strong>Resumen:</Text>
              <ul>
                <li>Las desviaciones en Costo de Ventas superan el umbral de alerta en 2 periodos</li>
                <li>Las ventas tuvieron desviaciones negativas en Febrero</li>
                <li>El gasto en publicidad se mantuvo por debajo del presupuesto</li>
              </ul>
            </div>
          </Card>
        </TabPane>
        
        <TabPane tab="Detalle de Desviaciones" key="details">
          <Card className="dashboard-card">
            <Table 
              dataSource={deviationData} 
              columns={columnasDesviaciones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Registrar Nueva Desviación"
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
          onFinish={handleGuardarDesviacion}
        >
          <Form.Item name="periodo" label="Periodo" rules={[{ required: true, message: 'Seleccione el periodo' }]}>
            <DatePicker picker="month" style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="cuenta" label="Cuenta" rules={[{ required: true, message: 'Seleccione la cuenta' }]}>
            <Select placeholder="Seleccione la cuenta">
              <Option value="ventas">Ventas</Option>
              <Option value="costo_ventas">Costo de Ventas</Option>
              <Option value="publicidad">Publicidad</Option>
              <Option value="sueldos">Sueldos</Option>
              <Option value="alquiler">Alquiler</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="real" label="Valor Real" rules={[{ required: true, message: 'Ingrese el valor real' }]}>
                <InputNumber 
                  placeholder="Valor real registrado"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="presupuesto" label="Valor Presupuestado" rules={[{ required: true, message: 'Ingrese el valor presupuestado' }]}>
                <InputNumber 
                  placeholder="Valor presupuestado"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción de la desviación y posibles causas" rows={4} />
          </Form.Item>
          
          <Form.Item name="analisis" label="Análisis de la Desviación">
            <TextArea placeholder="Análisis detallado de la desviación y posibles consecuencias" rows={4} />
          </Form.Item>
          
          <Form.Item name="accion_correctiva" label="Acción Correctiva">
            <TextArea placeholder="Acciones propuestas para corregir la desviación" rows={4} />
          </Form.Item>
          
          <Form.Item name="alerta" label="¿Requiere Alerta?" valuePropName="checked">
            <Select placeholder="Seleccione si requiere alerta">
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
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
                Registrar Desviación
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default DeviationAnalysis;