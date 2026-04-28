import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  HistoryOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
  UserOutlined,
  ClockCircleOutlined,
  DiffOutlined,
  DownloadOutlined,
  CopyOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const VersionControl: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('documents');
  const [form] = Form.useForm();
  
  // Datos simulados para documentos
  const documentData = [
    { id: '1', nombre: 'Manual de Usuario.pdf', tipo: 'documento', tamano: '2.4 MB', version: 'v3.2', autor: 'Carlos Gómez', fecha: '2023-04-15', estado: 'activo' },
    { id: '2', nombre: 'Catálogo de Productos.xlsx', tipo: 'hoja_calculo', tamano: '1.8 MB', version: 'v1.7', autor: 'María López', fecha: '2023-04-12', estado: 'activo' },
    { id: '3', nombre: 'Procedimiento Calidad.docx', tipo: 'documento', tamano: '0.9 MB', version: 'v2.1', autor: 'Ana Martínez', fecha: '2023-04-10', estado: 'obsoleto' },
    { id: '4', nombre: 'Reporte Anual.pptx', tipo: 'presentacion', tamano: '5.2 MB', version: 'v4.0', autor: 'Luis Fernández', fecha: '2023-04-08', estado: 'activo' },
  ];

  // Datos simulados para versiones
  const versionData = [
    { id: '1', documento: 'Manual de Usuario.pdf', version: 'v3.2', autor: 'Carlos Gómez', fecha: '2023-04-15', descripcion: 'Actualización de instrucciones de uso' },
    { id: '2', documento: 'Manual de Usuario.pdf', version: 'v3.1', autor: 'Carlos Gómez', fecha: '2023-03-20', descripcion: 'Corrección de errores tipográficos' },
    { id: '3', documento: 'Manual de Usuario.pdf', version: 'v3.0', autor: 'Carlos Gómez', fecha: '2023-02-10', descripcion: 'Revisión completa del contenido' },
    { id: '4', documento: 'Catálogo de Productos.xlsx', version: 'v1.7', autor: 'María López', fecha: '2023-04-12', descripcion: 'Actualización de precios y existencias' },
  ];

  const columnasDocumentos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let icon = null;
        if (tipo === 'documento') icon = <FileTextOutlined />;
        if (tipo === 'hoja_calculo') icon = <DiffOutlined />;
        if (tipo === 'presentacion') icon = <FolderOpenOutlined />;
        return <span>{icon} {tipo}</span>;
      }
    },
    { title: 'Tamaño', dataIndex: 'tamano', key: 'tamano' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    { title: 'Autor', dataIndex: 'autor', key: 'autor' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
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
          <Button type="link" icon={<DownloadOutlined />}>Descargar</Button>
          <Button type="link" icon={<HistoryOutlined />}>Historial</Button>
          <Button type="link" icon={<CopyOutlined />}>Copiar</Button>
        </Space>
      ),
    },
  ];

  const columnasVersiones = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Documento', dataIndex: 'documento', key: 'documento' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    { title: 'Autor', dataIndex: 'autor', key: 'autor' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<DownloadOutlined />}>Descargar</Button>
          <Button type="link" icon={<EditOutlined />}>Restaurar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearDocumento = () => {
    setModalVisible(true);
  };

  const handleGuardarDocumento = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear documento:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><HistoryOutlined /> Control de Versiones</Title>
          <Text>
            Seguimiento de cambios en documentos y registros del sistema
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearDocumento}>
            Nuevo Documento
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Documentos"
              value={142}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Versiones"
              value={847}
              prefix={<HistoryOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Usuarios"
              value={42}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Espacio Usado"
              value={12.4}
              precision={1}
              suffix="GB"
              prefix={<FolderOpenOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="documents" onChange={setActiveTab}>
        <TabPane tab="Documentos" key="documents">
          <Card className="dashboard-card">
            <Table 
              dataSource={documentData} 
              columns={columnasDocumentos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Historial de Versiones" key="versions">
          <Card className="dashboard-card">
            <Table 
              dataSource={versionData} 
              columns={columnasVersiones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Documento"
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
          onFinish={handleGuardarDocumento}
        >
          <Form.Item name="nombre" label="Nombre del Documento" rules={[{ required: true, message: 'Ingrese el nombre del documento' }]}>
            <Input placeholder="Ej: Manual de Usuario.pdf" />
          </Form.Item>
          
          <Form.Item name="tipo" label="Tipo de Documento" rules={[{ required: true, message: 'Seleccione el tipo de documento' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="documento">Documento (Word, PDF)</Option>
              <Option value="hoja_calculo">Hoja de Cálculo (Excel)</Option>
              <Option value="presentacion">Presentación (PowerPoint)</Option>
              <Option value="imagen">Imagen (JPEG, PNG)</Option>
              <Option value="otro">Otro</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Breve descripción del contenido del documento" rows={4} />
          </Form.Item>
          
          <Form.Item name="categoria" label="Categoría">
            <Select placeholder="Seleccione la categoría">
              <Option value="procedimientos">Procedimientos</Option>
              <Option value="manuales">Manuales</Option>
              <Option value="reportes">Reportes</Option>
              <Option value="politicas">Políticas</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="etiquetas" label="Etiquetas">
            <Select 
              mode="tags" 
              placeholder="Agregue etiquetas relevantes"
              dropdownRender={() => null}
            >
            </Select>
          </Form.Item>
          
          <Form.Item name="permisos" label="Permisos de Acceso" rules={[{ required: true, message: 'Seleccione los permisos de acceso' }]}>
            <Select placeholder="Seleccione los permisos">
              <Option value="lectura">Solo lectura</Option>
              <Option value="escritura">Lectura y escritura</Option>
              <Option value="administrador">Administrador</Option>
              <Option value="personalizado">Personalizado</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="archivo" label="Archivo">
            <input type="file" />
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
                Subir Documento
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default VersionControl;