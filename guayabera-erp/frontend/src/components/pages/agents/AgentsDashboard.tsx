import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, message } from 'antd';
import { 
  PlusOutlined, 
  DesktopOutlined, 
  PrinterOutlined, 
  ToolOutlined, 
  SyncOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const AgentsDashboard: React.FC = () => {
  const [agents, setAgents] = useState<any[]>([
    { 
      key: '1', 
      id: 'AGT-001', 
      nombre_maquina: 'PC-Diseño-01', 
      tipo: 'CAD', 
      ip: '192.168.1.101', 
      so: 'Windows 10', 
      estado: 'Conectado', 
      ultima_conexion: '2023-04-01 10:30:00', 
      version: '1.0.0' 
    },
    { 
      key: '2', 
      id: 'AGT-002', 
      nombre_maquina: 'PC-Impresión-01', 
      tipo: 'PRINT', 
      ip: '192.168.1.102', 
      so: 'Windows 11', 
      estado: 'Conectado', 
      ultima_conexion: '2023-04-01 11:45:00', 
      version: '1.0.0' 
    },
    { 
      key: '3', 
      id: 'AGT-003', 
      nombre_maquina: 'PC-Diseño-02', 
      tipo: 'DESIGN', 
      ip: '192.168.1.103', 
      so: 'Windows 10', 
      estado: 'Desconectado', 
      ultima_conexion: '2023-03-31 18:20:00', 
      version: '0.9.8' 
    },
  ]);
  
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [currentAgent, setCurrentAgent] = useState<any>(null);
  const [form] = Form.useForm();

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre de Máquina', dataIndex: 'nombre_maquina', key: 'nombre_maquina' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let icon, color;
        switch(tipo) {
          case 'CAD':
            icon = <ToolOutlined />;
            color = 'blue';
            break;
          case 'PRINT':
            icon = <PrinterOutlined />;
            color = 'green';
            break;
          case 'DESIGN':
            icon = <DesktopOutlined />;
            color = 'purple';
            break;
          default:
            icon = <DesktopOutlined />;
            color = 'default';
        }
        return <Tag icon={icon} color={color}>{tipo}</Tag>;
      }
    },
    { title: 'IP', dataIndex: 'ip', key: 'ip' },
    { title: 'SO', dataIndex: 'so', key: 'so' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Conectado') color = 'green';
        if (estado === 'Desconectado') color = 'red';
        return <Tag icon={estado === 'Conectado' ? <CheckCircleOutlined /> : <CloseCircleOutlined />} color={color}>{estado}</Tag>;
      }
    },
    { title: 'Última Conexión', dataIndex: 'ultima_conexion', key: 'ultima_conexion' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Editar
          </Button>
          <Button 
            type="link" 
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.key)}
          >
            Eliminar
          </Button>
        </Space>
      ),
    },
  ];

  const handleEdit = (agent: any) => {
    setCurrentAgent(agent);
    form.setFieldsValue({
      nombre_maquina: agent.nombre_maquina,
      tipo: agent.tipo,
      ip: agent.ip,
      so: agent.so,
      version: agent.version,
    });
    setIsModalVisible(true);
  };

  const handleDelete = (key: string) => {
    Modal.confirm({
      title: '¿Está seguro de eliminar este agente?',
      content: 'Esta acción no se puede deshacer.',
      okText: 'Sí',
      cancelText: 'No',
      onOk: () => {
        setAgents(agents.filter(agent => agent.key !== key));
        message.success('Agente eliminado correctamente');
      }
    });
  };

  const handleSave = () => {
    form.validateFields().then(values => {
      if (currentAgent) {
        // Actualizar agente existente
        const updatedAgents = agents.map(agent => 
          agent.key === currentAgent.key 
            ? { ...agent, ...values } 
            : agent
        );
        setAgents(updatedAgents);
      } else {
        // Agregar nuevo agente
        const newAgent = {
          key: `${agents.length + 1}`,
          id: `AGT-${(agents.length + 1).toString().padStart(3, '0')}`,
          ...values,
          estado: 'Desconectado',
          ultima_conexion: new Date().toISOString().slice(0, 19).replace('T', ' '),
        };
        setAgents([...agents, newAgent]);
      }
      message.success(`Agente ${currentAgent ? 'actualizado' : 'creado'} correctamente`);
      setIsModalVisible(false);
      form.resetFields();
      setCurrentAgent(null);
    });
  };

  const showModal = () => {
    setCurrentAgent(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <Title level={2}>Gestión de Agentes Locales</Title>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={showModal}
        >
          Nuevo Agente
        </Button>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Total Agentes" 
              value={agents.length} 
              prefix={<DesktopOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Conectados" 
              value={agents.filter(a => a.estado === 'Conectado').length} 
              prefix={<SyncOutlined spin />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Desconectados" 
              value={agents.filter(a => a.estado === 'Desconectado').length} 
              prefix={<CloseCircleOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Tipos Diferentes" 
              value={[...new Set(agents.map(a => a.tipo))].length} 
              prefix={<ToolOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table 
          dataSource={agents} 
          columns={columns} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={currentAgent ? "Editar Agente" : "Nuevo Agente"}
        open={isModalVisible}
        onOk={handleSave}
        onCancel={() => {
          setIsModalVisible(false);
          form.resetFields();
          setCurrentAgent(null);
        }}
        okText="Guardar"
        cancelText="Cancelar"
      >
        <Form
          form={form}
          layout="vertical"
          name="agent_form"
        >
          <Form.Item
            name="nombre_maquina"
            label="Nombre de Máquina"
            rules={[{ required: true, message: 'Por favor ingrese el nombre de la máquina' }]}
          >
            <Input placeholder="Ej: PC-Diseño-01" />
          </Form.Item>
          
          <Form.Item
            name="tipo"
            label="Tipo de Agente"
            rules={[{ required: true, message: 'Por favor seleccione el tipo de agente' }]}
          >
            <Select placeholder="Seleccione el tipo">
              <Option value="CAD">CAD (Diseño Técnico)</Option>
              <Option value="PRINT">PRINT (Impresión)</Option>
              <Option value="DESIGN">DESIGN (Diseño Gráfico)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            name="ip"
            label="Dirección IP"
            rules={[
              { required: true, message: 'Por favor ingrese la dirección IP' },
              { pattern: /^(\d{1,3}\.){3}\d{1,3}$/, message: 'Dirección IP inválida' }
            ]}
          >
            <Input placeholder="Ej: 192.168.1.101" />
          </Form.Item>
          
          <Form.Item
            name="so"
            label="Sistema Operativo"
            rules={[{ required: true, message: 'Por favor ingrese el sistema operativo' }]}
          >
            <Input placeholder="Ej: Windows 10, macOS 12, Ubuntu 20.04" />
          </Form.Item>
          
          <Form.Item
            name="version"
            label="Versión del Agente"
            rules={[{ required: true, message: 'Por favor ingrese la versión del agente' }]}
          >
            <Input placeholder="Ej: 1.0.0" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default AgentsDashboard;