import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Modal, Form, Input, Select, message, Tag, Card, Row, Col, Statistic } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined, SearchOutlined } from '@ant-design/icons';
import supplyChainApi, { Proveedor } from '../../../services/supplyChainApi';

const { Option } = Select;

const ProveedoresPage: React.FC = () => {
  const [proveedores, setProveedores] = useState<Proveedor[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingProveedor, setEditingProveedor] = useState<Proveedor | null>(null);
  const [form] = Form.useForm();
  const [searchText, setSearchText] = useState('');

  const fetchProveedores = async () => {
    setLoading(true);
    try {
      const data = await supplyChainApi.getProveedores();
      setProveedores(data);
    } catch (error) {
      message.error('Error al cargar proveedores');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProveedores();
  }, []);

  const handleCreate = () => {
    setEditingProveedor(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Proveedor) => {
    setEditingProveedor(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '¿Eliminar proveedor?',
      content: 'Esta acción no se puede deshacer',
      onOk: async () => {
        try {
          await supplyChainApi.deleteProveedor(id);
          message.success('Proveedor eliminado');
          fetchProveedores();
        } catch (error) {
          message.error('Error al eliminar proveedor');
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingProveedor) {
        await supplyChainApi.updateProveedor(editingProveedor.id, values);
        message.success('Proveedor actualizado');
      } else {
        await supplyChainApi.createProveedor(values);
        message.success('Proveedor creado');
      }
      setModalVisible(false);
      fetchProveedores();
    } catch (error) {
      message.error('Error al guardar proveedor');
    }
  };

  const columns = [
    {
      title: 'Código',
      dataIndex: 'codigo',
      key: 'codigo',
      sorter: (a: Proveedor, b: Proveedor) => a.codigo.localeCompare(b.codigo),
    },
    {
      title: 'Nombre Comercial',
      dataIndex: 'nombre_comercial',
      key: 'nombre_comercial',
      render: (text: string) => <strong>{text}</strong>,
    },
    {
      title: 'RFC',
      dataIndex: 'rfc',
      key: 'rfc',
    },
    {
      title: 'Tipo',
      dataIndex: 'tipo_proveedor',
      key: 'tipo_proveedor',
      render: (tipo: string) => {
        const colors: Record<string, string> = {
          nacional: 'blue',
          extranjero: 'purple',
          cliente_proveedor: 'green',
        };
        return <Tag color={colors[tipo] || 'default'}>{tipo.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Contacto',
      key: 'contacto',
      render: (_: any, record: Proveedor) => (
        <div>
          <div>{record.correo_electronico}</div>
          <div>{record.telefono}</div>
        </div>
      ),
    },
    {
      title: 'Estado',
      dataIndex: 'activo',
      key: 'activo',
      render: (activo: boolean) => (
        <Tag color={activo ? 'success' : 'default'}>
          {activo ? 'ACTIVO' : 'INACTIVO'}
        </Tag>
      ),
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_: any, record: Proveedor) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleEdit(record)}
          />
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          />
        </Space>
      ),
    },
  ];

  const filteredProveedores = proveedores.filter((p) =>
    p.nombre_comercial.toLowerCase().includes(searchText.toLowerCase()) ||
    p.codigo.toLowerCase().includes(searchText.toLowerCase()) ||
    p.rfc.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div style={{ padding: '24px' }}>
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Statistic 
              title="Total Proveedores" 
              value={proveedores.length}
              prefix="📦"
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="Activos" 
              value={proveedores.filter(p => p.activo).length}
              prefix="✅"
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="Nacionales" 
              value={proveedores.filter(p => p.tipo_proveedor === 'nacional').length}
              prefix="🇲🇽"
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="Extranjeros" 
              value={proveedores.filter(p => p.tipo_proveedor === 'extranjero').length}
              prefix="🌎"
            />
          </Col>
        </Row>
      </Card>

      <Card
        title="Gestión de Proveedores"
        extra={
          <Space>
            <Input
              placeholder="Buscar proveedor..."
              prefix={<SearchOutlined />}
              style={{ width: 300 }}
              onChange={(e) => setSearchText(e.target.value)}
            />
            <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
              Nuevo Proveedor
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={filteredProveedores}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingProveedor ? 'Editar Proveedor' : 'Nuevo Proveedor'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={700}
      >
        <Form form={form} layout="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="codigo"
                label="Código"
                rules={[{ required: true, message: 'Ingrese el código' }]}
              >
                <Input placeholder="Ej: PROV001" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="rfc"
                label="RFC"
                rules={[
                  { required: true, message: 'Ingrese el RFC' },
                  { len: 12, message: 'El RFC debe tener 12 caracteres' },
                ]}
              >
                <Input placeholder="Ej: PTS900101ABC" maxLength={13} />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="nombre_comercial"
            label="Nombre Comercial"
            rules={[{ required: true, message: 'Ingrese el nombre comercial' }]}
          >
            <Input placeholder="Nombre comercial del proveedor" />
          </Form.Item>

          <Form.Item name="razon_social" label="Razón Social">
            <Input placeholder="Razón social completa" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="correo_electronico" label="Correo Electrónico">
                <Input type="email" placeholder="correo@ejemplo.com" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="telefono" label="Teléfono">
                <Input placeholder="9991234567" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="tipo_proveedor"
                label="Tipo de Proveedor"
                rules={[{ required: true }]}
                initialValue="nacional"
              >
                <Select>
                  <Option value="nacional">Nacional</Option>
                  <Option value="extranjero">Extranjero</Option>
                  <Option value="cliente_proveedor">Cliente-Proveedor</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="activo" label="Estado" initialValue={true} valuePropName="checked">
                <Select>
                  <Option value={true}>Activo</Option>
                  <Option value={false}>Inactivo</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ProveedoresPage;
